# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.config import Config
from main_pack.api.commerce import api
import requests,json

# Users and auth
from main_pack.models.users.models import Users
from main_pack.api.auth.api_login import token_required
# / Users and auth /

# Orders
from main_pack.models.commerce.models import Order_inv,Order_inv_line,Work_period
from main_pack.api.commerce.utils import addOrderInvDict,addOrderInvLineDict
from main_pack.base.invoiceMethods import get_order_error_type
from main_pack.base.apiMethods import checkApiResponseStatus
# / Orders /

from datetime import datetime,timezone
from main_pack.key_generator.utils import generate,makeRegNo,Pred_regnum

# Resource models and operations
from main_pack.models.commerce.models import Resource,Res_price,Res_total
from main_pack.base.invoiceMethods import totalQtySubstitution
from main_pack.base.num2text import num2text,price2text
import decimal
# / Resource models and operations /


@api.route("/checkout-sale-order-inv/",methods=['POST'])
@token_required
def api_checkout_sale_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	work_period = Work_period.query\
		.filter_by(GCRecord = None, WpIsDefault = True)\
		.first()
	# !!! current user is rp_acc if type is rp_acc
	if model_type == 'Rp_acc':
		name = current_user.RpAccUName
		RpAccId = current_user.RpAccId
		DivId = current_user.DivId
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
		orderRegNo = req['orderInv']['OInvRegNo']
		InvStatId = req['orderInv']['InvStatId']
		reg_num_pred_exists = None

		##### check if invoice is not empty #####
		if not req['orderInv']['OrderInvLines']:
			raise Exception

		if not orderRegNo:
			######## generate reg no ########
			try:
				reg_num = generate(UId=user.UId,RegNumTypeName='sale_order_invoice_code')
				orderRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
			except Exception as ex:
				print(f"{datetime.now()} | Checkout OInv Exception: {ex}. Couldn't generate RegNo using User's credentials")
				# use device model and other info
				orderRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
		else:
			reg_num_pred_exists = Pred_regnum.query\
				.filter_by(GCRecord = None, RegNum = orderRegNo).first()
			if not reg_num_pred_exists:
				raise Exception

		###### order inv setup ######
		order_invoice['OInvRegNo'] = orderRegNo
		order_invoice['InvStatId'] = 1
		order_invoice['OInvTypeId'] = 2
		order_invoice['WpId'] = work_period.WpId
		order_invoice['WhId'] = 1
		order_invoice['DivId'] = DivId
		if InvStatId == 13:
			order_invoice['InvStatId'] = InvStatId

		# default currency is 1 TMT of not specified
		if not order_invoice['CurrencyId']:
			order_invoice['CurrencyId'] = 1
		order_invoice['RpAccId'] = RpAccId

		newOrderInv = Order_inv(**order_invoice)
		db.session.add(newOrderInv)

		order_inv_lines = []
		failed_order_inv_lines = []
		OInvTotal = 0
		OrderInvLines = req['orderInv']['OrderInvLines']
		for order_inv_line_req in OrderInvLines:
			try:
				# in case of errors, the error_type is provided
				error_type = 0
				order_inv_line = addOrderInvLineDict(order_inv_line_req)
				# OInvLineRegNo generation
				try:
					reg_num = generate(UId=user.UId,RegNumTypeName='order_invoice_line_code')
					orderLineRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
				except Exception as ex:
					print(f"{datetime.now()} | Checkout OInv Exception: {ex}. Couldn't generate RegNo using User's credentials")
					# use device model and other info
					orderLineRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
				order_inv_line['OInvLineRegNo'] = orderLineRegNo
				orderLineRegNo = None

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
					.filter_by(GCRecord = None, ResId = ResId, ResPriceTypeId = 2)\
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
				order_inv_line['UnitId'] = resource.UnitId
				if not order_inv_line['CurrencyId']:
					order_inv_line['CurrencyId'] = 1
				
				# increment of Main Order Inv Total Price
				OInvTotal += OInvLineFTotal

				thisOInvLine = Order_inv_line(**order_inv_line)
				db.session.add(thisOInvLine)
				order_inv_lines.append(thisOInvLine.to_json_api())

				order_inv_line = None
			except Exception as ex:
				print(f"{datetime.now()} | Checkout OInv Line Exception: {ex} | Error type {error_type}")
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
				res[e] = status[e]
		
		else:
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,
				Config.PRICE_2_TEXT_LANGUAGE,
				Config.PRICE_2_TEXT_CURRENCY)

			newOrderInv.OInvTotal = decimal.Decimal(OInvTotal)
			newOrderInv.OInvFTotal = decimal.Decimal(OInvFTotal)
			newOrderInv.OInvFTotalInWrite = OInvFTotalInWrite

			if reg_num_pred_exists:
				db.session.delete(reg_num_pred_exists)

			db.session.commit()

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
				res[e] = status[e]

	except Exception as ex:
		print(f"{datetime.now()} | Checkout OInv Exception: {ex}")
		status_code = 400
		res = {
			"data": order_invoice,
			"message": "Failed to checkout order"
		}	
	response = make_response(jsonify(res),status_code)

	return response


@api.route("/validate-order-inv-payment/",methods=['GET','POST'])
@token_required
def validate_order_inv_payment(user):
	current_user = user['current_user']
	RpAccId = current_user.RpAccId

	if request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			OInvRegNo = req["OInvRegNo"]
			OrderId = req["OrderId"]
			
			status = 0
			message = ''
			data = {}

			if OrderId:
				order_inv = Order_inv.query\
					.filter_by(
						RpAccId = RpAccId,
						OInvRegNo = OInvRegNo,
						GCRecord = None)\
					.first()

				if order_inv:
					# if order isn't already paid
					if order_inv.PaymStatusId != 2:
						try:
							r = requests.get(f"{Config.ORDER_VALIDATION_SERVICE_URL}?orderId={OrderId}&password={Config.ORDER_VALIDATION_SERVICE_PASSWORD}&userName={Config.ORDER_VALIDATION_SERVICE_USERNAME}")
							response_json = json.loads(r.text)

							if (str(response_json[Config.ORDER_VALIDATION_KEY]) == str(Config.ORDER_VALIDATION_VALUE)):
								PaymentAmount = int(response_json["Amount"])/100
								order_inv.OInvPaymAmount = PaymentAmount
								order_inv.InvStatId = 1
								if (PaymentAmount >= order_inv.OInvFTotal):
									order_inv.PaymStatusId = 2
								elif (PaymentAmount < order_inv.OInvFTotal and PaymentAmount > 0):
									order_inv.PaymStatusId = 3
								message = "Payment Validation: success"

							else:
								# invoice status = "Payment fail"
								# Payment status = "Not paid"
								order_inv.PaymStatusId = 1
								order_inv.OInvPaymAmount = 0
								order_inv.InvStatId = 14

								message = f"Payment Validation: failed (OrderStatus = {response_json[Config.ORDER_VALIDATION_KEY]})"
								print(f"{datetime.now()} | {message}")
							
							order_inv.AddInf5 = str(response_json)
							db.session.commit()
							data = response_json
							status = 1
						
						except Exception as ex:
							message = "Payment Validation: failed (Connection error)"
							print(f"{datetime.now()} | Payment Validation Exception: {ex}")

							req["message"] = message
							order_inv.AddInf5 = str(req)
							order_inv.InvStatId = 14
							db.session.commit()

					else:
						message = "Already paid"

				else:
					message = "Payment Validation: failed (Order_inv is None)"
					print(f"{datetime.now()} | {message}")
					
			else:
				message = "Payment Validation: failed (OrderId is None)"
				print(f"{datetime.now()} | {message}")

			res = {
				"data": data,
				"message": message,
				"status": status,
				"total": len(data)
			}

			if res['status'] == 0:
				status_code = 200
			else:
				status_code = 201
			response = make_response(jsonify(res),status_code)
	return response