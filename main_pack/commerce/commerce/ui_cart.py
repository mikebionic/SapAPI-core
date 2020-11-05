from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.commerce import bp
from main_pack.config import Config
import os
import uuid

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.languageMethods import dataLangSelector
from sqlalchemy import and_
import decimal
from main_pack.base.num2text import num2text,price2text
from main_pack.base.invoiceMethods import totalQtySubstitution
# / useful methods /

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.admin.utils import resRelatedData
# / Resource and view /

# users and customers
from main_pack.models.users.models import Users, Rp_acc
# / users and customers /

# Invoices
from main_pack.api.commerce.commerce_utils import UiCartResourceData
from main_pack.models.base.models import Warehouse
from main_pack.models.commerce.models import (
	Resource,
	Order_inv,
	Order_inv_line,
	Work_period,
	Res_price,
	Res_total)
from main_pack.commerce.commerce.order_utils import addOInvLineDict
# / Invoices /

# RegNo
from main_pack.key_generator.utils import makeRegNo,generate,validate
from datetime import datetime,timezone
# / RegNo /

@bp.route("/product/ui_cart/", methods=['POST','PUT'])
def ui_cart():
	product_list = []
	if request.method == 'POST':
		try:
			req = request.get_json()
			ResId = req.get('resId')
			productQty = req.get('productQty')

			product = {}
			product['ResId'] = ResId
			product['productQty'] = productQty
			product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Product')+' '+gettext('successfully saved'),
				"htmlData": render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cartItemAppend.html",
					**resData)
				})
		except Exception as ex:
			response = jsonify({
				"status": 'error',
				"responseText": gettext('Unknown error!'),
				})

	elif request.method == 'PUT':
		req = request.get_json()
		try:
			for resElement in req:
				ResId = req[resElement].get('resId')
				productQty = req[resElement].get('productQty')
				
				product={}
				product['ResId'] = ResId
				product['productQty'] = productQty
				product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Product')+' '+gettext('successfully saved'),
				"htmlData": render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cartItemAppend.html",
					**resData)
				})
		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": 'error',
				"responseText": gettext('Unknown error!'),
				})
	return response

@bp.route("/product/ui_cart_table/", methods=['POST','PUT'])
def ui_cart_table():
	product_list=[]
	if request.method == 'POST':
		try:
			req = request.get_json()
			ResId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['ResId'] = ResId
			product['productQty'] = productQty
			product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Product')+' '+gettext('successfully saved'),
				"htmlData": render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cartTableAppend.html",
					**resData)
				})
		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": 'error',
				"responseText": gettext('Unknown error!'),
				})

	elif request.method == 'PUT':
		req = request.get_json()
		try:
			for resElement in req:
				ResId = req[resElement].get('resId')
				productQty = req[resElement].get('productQty')
				
				product={}
				product['ResId'] = ResId
				product['productQty'] = productQty
				product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Product')+' '+gettext('successfully saved'),
				"htmlData": render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cartTableAppend.html",
					**resData)
				})
		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": 'error',
				"responseText": gettext('Unknown error!'),
				})
	return response

# Expected JSON
# {
# 	"cartData": {
# 		"product5": {
# 			"resId": '5',
# 			"priceValue": '9.5',
# 			"productQty": 1
# 		},
# 		"product8": {
# 			"resId": '8',
# 			"priceValue": '10.0',
# 			"productQty": 1
# 		}
# 	}, 
# 	"orderDesc": ''
# }

@bp.route("/product/ui_cart_checkout/",methods=['POST'])
@login_required
def ui_cart_checkout():
	if request.method == 'POST':
		req = request.get_json()
		try:
			if not req['cartData']:
				# no products in cart
				raise Exception

			work_period = Work_period.query\
				.filter_by(GCRecord = None, WpIsDefault = True)\
				.first()

			# get the rp_acc of current logged user
			rp_acc = Rp_acc.query\
				.filter_by(GCRecord = None, RpAccId = current_user.RpAccId)\
				.first()

			user = Users.query\
				.filter_by(GCRecord = None, UId = rp_acc.UId)\
				.first()
			if user is None:
				# try to find the rp_acc registered user if no seller specified
				user = Users.query\
					.filter_by(GCRecord = None, RpAccId = rp_acc.RpAccId)\
					.first()

			######## generate reg no ########
			try:
				reg_num = generate(UId=user.UId,RegNumTypeName='sale_order_invoice_code')
				orderRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
			except Exception as ex:
				print(ex)
				# use device model and other info
				orderRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())			


			DivId = current_user.DivId
			CId = current_user.CId
			warehouse = Warehouse.query\
				.filter_by(DivId = DivId, GCRecord = None)\
				.order_by(Warehouse.WhId.asc())\
				.first()
			WhId = warehouse.WhId if warehouse else None

			OInvDesc = req.get('orderDesc')
			
			order_invoice = {
				"OInvTypeId": 2,
				"OInvGuid": uuid.uuid4(),
				"InvStatId": 1,
				"CurrencyId": 1,
				"WhId": WhId,
				"DivId": DivId,
				"CId": CId,
				"WpId": work_period.WpId,
				"RpAccId": rp_acc.RpAccId,
				"OInvRegNo": orderRegNo,
				"OInvDesc": OInvDesc
			}

			orderInv = Order_inv(**order_invoice)
			db.session.add(orderInv)
			OInvTotal = 0
			order_inv_lines = []
			failed_order_inv_lines = []		
			for resElement in req['cartData']:
				ResId = int(req['cartData'][resElement].get('resId'))
				OInvLineAmount = int(req['cartData'][resElement].get('productQty'))

				resource = Resource.query\
					.filter_by(GCRecord = None, ResId = ResId)\
					.first()
				res_total = Res_total.query\
					.filter_by(GCRecord = None, ResId = ResId)\
					.first()
				totalSubstitutionResult = totalQtySubstitution(res_total.ResPendingTotalAmount,OInvLineAmount)
				try:
					if not resource or totalSubstitutionResult['status'] == 0:
						raise Exception

					resourceInv = resource.to_json_api()
					OInvLineAmount = totalSubstitutionResult['amount']
					res_total.ResPendingTotalAmount = totalSubstitutionResult['totalBalance']

					res_price = Res_price.query\
						.filter_by(GCRecord = None, ResId = resource.ResId, ResPriceTypeId = 2)\
						.first()
					OInvLinePrice = float(res_price.ResPriceValue) if res_price else 0
					OInvLineTotal = OInvLinePrice*OInvLineAmount

					# add taxes and stuff later on
					OInvLineFTotal = OInvLineTotal
					
					###### inv line assignment ######
					resourceInv['OInvLineAmount'] = OInvLineAmount
					resourceInv['OInvLinePrice'] = decimal.Decimal(OInvLinePrice)
					resourceInv['OInvLineTotal'] = decimal.Decimal(OInvLineTotal)
					resourceInv['OInvLineFTotal'] = decimal.Decimal(OInvLineFTotal)
					resourceInv['OInvId'] = orderInv.OInvId
					resourceInv['UnitId'] = resource.UnitId
					if not 'CurrencyId' in resourceInv:
						resourceInv['CurrencyId'] = 1
					
					order_inv_line = addOInvLineDict(resourceInv)

					# OInvLineRegNo generation
					try:
						reg_num = generate(UId=user.UId,RegNumTypeName='order_invoice_line_code')
						orderLineRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
					except Exception as ex:
						print(ex)
						# use device model and other info
						orderLineRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
					order_inv_line['OInvLineRegNo'] = orderLineRegNo
					order_inv_line['OInvLineGuid'] = uuid.uuid4()
					
					# increment of Main Order Inv Total Price
					OInvTotal += OInvLineFTotal

					thisOInvLine = Order_inv_line(**order_inv_line)
					db.session.add(thisOInvLine)			
					order_inv_lines.append(thisOInvLine.to_json_api())
				except Exception as ex:
					print(ex)
					failed_order_inv_lines.append(req['cartData'][resElement])

			if (len(order_inv_lines) == 0):
				raise Exception
			###### final order assignment and processing ######
			# add taxes and stuff later on
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,
				Config.PRICE_2_TEXT_LANGUAGE,
				Config.PRICE_2_TEXT_CURRENCY)

			orderInv.OInvTotal = decimal.Decimal(OInvTotal)
			orderInv.OInvFTotal = decimal.Decimal(OInvFTotal)
			orderInv.OInvFTotalInWrite = OInvFTotalInWrite

			db.session.commit()

			response = jsonify({
				"status": 'added',
				"responseText": gettext('Checkout')+' '+gettext('successfully done')+'! '+gettext('View orders in profile page.')
				})

		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": 'error',
				"responseText": gettext('Unknown error!')
				})
	return response
