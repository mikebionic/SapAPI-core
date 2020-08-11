# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.base.invoiceMethods import get_order_error_type

from main_pack.models.users.models import Users
from main_pack.models.commerce.models import Order_inv,Order_inv_line,Work_period
from main_pack.api.commerce.utils import addOrderInvDict,addOrderInvLineDict
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.config import Config
from datetime import datetime,timezone
from main_pack.api.auth.api_login import token_required

from main_pack.models.commerce.models import Resource,Res_price,Res_total
from main_pack.base.invoiceMethods import totalQtySubstitution
from main_pack.base.num2text import num2text,price2text
from sqlalchemy import and_
from main_pack.key_generator.utils import generate,makeRegNo
import decimal

@api.route("/checkout-sale-order-inv/",methods=['POST'])
@token_required
def api_checkout_sale_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	work_period = Work_period.query\
		.filter_by(GCRecord = None, WpIsDefault = True)\
		.first()
	# !!! current user is rp_acc if type is rp_acc
	if model_type=='Rp_acc':
		name = current_user.RpAccUName
		RpAccId = current_user.RpAccId
		# get the seller's user information of a specific rp_acc
		user = Users.query\
			.filter_by(GCRecord = None, UId = current_user.UId)\
			.first()
		if user is None:
			# try to find the rp_acc registered user if no seller specified
			user = Users.query\
				.filter_by(GCRecord = None, RpAccId = RpAccId)\
				.first()
	try:
		req = request.get_json()
		order_invoice = addOrderInvDict(req['orderInv'])

		##### check if invoice is not empty #####
		if not req['orderInv']['OrderInvLines']:
			raise Exception

		######## generate reg no ########
		try:
			reg_num = generate(UId=user.UId,prefixType='sale_order_invoice_code')
			orderRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
		except Exception as ex:
			print(ex)
			# use device model and other info
			orderRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())

		###### order inv setup ######
		order_invoice['OInvRegNo']=orderRegNo
		order_invoice['InvStatId']=1
		order_invoice['OInvTypeId']=2
		order_invoice['WpId']=work_period.WpId
		# default currency is 1 TMT of not specified
		if not order_invoice['CurrencyId']:
			order_invoice['CurrencyId']=1
		order_invoice['RpAccId']=RpAccId

		newOrderInv = Order_inv(**order_invoice)
		db.session.add(newOrderInv)

		order_inv_lines = []
		failed_order_inv_lines = []
		OInvTotal = 0
		OrderInvLines = req['orderInv']['OrderInvLines']
		for order_inv_line_req in OrderInvLines:
			try:
				# in case of errors, the error_type is provided
				error_type=0

				order_inv_line = addOrderInvLineDict(order_inv_line_req)

				# OInvLineRegNo generation
				try:
					reg_num = generate(UId=user.UId,prefixType='order_invoice_line_code')
					orderLineRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
				except Exception as ex:
					print(ex)
					# use device model and other info
					orderLineRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
				order_inv_line['OInvLineRegNo']=orderLineRegNo

				ResId = order_inv_line['ResId']
				OInvLineAmount = int(order_inv_line['OInvLineAmount'])
				resource = Resource.query\
					.filter_by(GCRecord = None, ResId = ResId)\
					.first()
				
				if not resource:
					# type deleted or none 
					error_type = 1
					raise Exception
				
				res_price = Res_price.query\
					.filter_by(GCRecord = None, ResId = resource.ResId, ResPriceTypeId = 2)\
					.first()
				res_total = Res_total.query\
					.filter_by(GCRecord = None, ResId = ResId, WhId = 1)\
					.first()
				totalSubstitutionResult = totalQtySubstitution(res_total.ResPendingTotalAmount,OInvLineAmount)


				if resource.UsageStatusId == 2:
					# resource unavailable or inactive
					error_type = 2
					raise Exception
				
				if totalSubstitutionResult['status'] == 0:
					# resource is empty or bad request with amount = -1
					error_type = 3
					raise Exception

				if order_inv_line['OInvLinePrice'] != res_price.ResPriceValue:
					error_type = 4
					raise Exception

				OInvLineAmount = totalSubstitutionResult['amount']
				# ResPendingTotalAmount is decreased but not ResTotBalance
				res_total.ResPendingTotalAmount = totalSubstitutionResult['totalBalance']
				############
				OInvLinePrice = float(res_price.ResPriceValue) if res_price else 0
				OInvLineTotal = OInvLinePrice*OInvLineAmount

				# add taxes and stuff later on
				OInvLineFTotal = OInvLineTotal
				
				###### inv line assignment ######
				order_inv_line['OInvLineAmount'] = decimal.Decimal(OInvLineAmount)
				order_inv_line['OInvLinePrice'] = decimal.Decimal(OInvLinePrice)
				order_inv_line['OInvLineTotal'] = decimal.Decimal(OInvLineTotal)
				order_inv_line['OInvLineFTotal'] = decimal.Decimal(OInvLineFTotal)
				order_inv_line['OInvId'] = newOrderInv.OInvId
				if not order_inv_line['CurrencyId']:
					order_inv_line['CurrencyId'] = 1
				
				# increment of Main Order Inv Total Price
				OInvTotal += OInvLineFTotal

				thisOInvLine = Order_inv_line(**order_inv_line)
				db.session.add(thisOInvLine)
				order_inv_lines.append(thisOInvLine.to_json_api())
			except Exception as ex:
				print(ex)
				fail_info = {
					"data": order_inv_line_req,
					"error_type_id": error_type,
					"error_type_message": get_order_error_type(error_type)
				}
				failed_order_inv_lines.append(fail_info)

		###### final order assignment and processing ######
		# add taxes and stuff later on
		if failed_order_inv_lines:
			status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)
			res = {
				"data": order_invoice,
				"successes": order_inv_lines,
				"fails": failed_order_inv_lines,
				"success_total": len(order_inv_lines),
				"fail_total": len(failed_order_inv_lines),
				"total": len(OrderInvLines)
			}
			status_code = 400
			for e in status:
				res[e]=status[e]
		
		else:
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,
																		Config.PRICE_2_TEXT_LANGUAGE,
																		Config.PRICE_2_TEXT_CURRENCY)

			newOrderInv.OInvTotal = decimal.Decimal(OInvTotal)
			newOrderInv.OInvFTotal = decimal.Decimal(OInvFTotal)
			newOrderInv.OInvFTotalInWrite = OInvFTotalInWrite

			db.session.commit()
			print("committed, done..")

			status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)
			res = {
				"data": newOrderInv.to_json_api(),
				"successes": order_inv_lines,
				"fails": failed_order_inv_lines,
				"success_total": len(order_inv_lines),
				"fail_total": len(failed_order_inv_lines),
				"total": len(OrderInvLines)
			}
			status_code = 200
			for e in status:
				res[e]=status[e]

	except Exception as ex:
		print(ex)
		status_code = 400
		res = {
			"data": order_invoice,
			"message": "Failed to checkout order"
		}	
	response = make_response(jsonify(res),status_code)

	return response