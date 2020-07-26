from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.admin import bp
import os
from flask import current_app

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
from main_pack.commerce.users.routes import ui_admin_required
# / auth and validation /

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import commonUsedData
from main_pack.commerce.admin.utils import resRelatedData
# / Resource and view /

# users and customers
from main_pack.models.users.models import (Users,
																					Rp_acc)
# / users and customers /

# Invoices
from main_pack.api.commerce.commerce_utils import UiCartResourceData
from main_pack.models.commerce.models import (Resource,
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
	product_list=[]
	if request.method == "POST":
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
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
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
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response

@bp.route("/product/ui_cart_table/", methods=['POST','PUT'])
def ui_cart_table():
	product_list=[]
	if request.method == "POST":
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
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
		resources=[]
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
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response

# Expected JSON
# {
# 	'cartData': {
# 		'product5':{
# 			'resId': '5',
# 			'priceValue': '9.5',
# 			'productQty': 1
# 		},
# 		'product8':{
# 			'resId': '8',
# 			'priceValue': '10.0',
# 			'productQty': 1
# 		}
# 	}, 
# 	'orderDesc': ''
# }

@bp.route("/product/ui_cart_checkout/",methods=['POST'])
@login_required
def ui_cart_checkout():
	if request.method == "POST":
		req = request.get_json()
		try:
			if not req['cartData']:
				# no products in cart
				raise Exception

			work_period = Work_period.query\
				.filter(and_(Work_period.GCRecord=='' or Work_period.GCRecord==None),\
					Work_period.WpIsDefault==True).first()

			# get the rp_acc of current logged user
			rp_acc = Rp_acc.query\
				.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
					Rp_acc.RpAccId==current_user.RpAccId).first()

			user = Users.query\
				.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
					Users.UId==rp_acc.UId).first()
			if user is None:
				# try to find the rp_acc registered user if no seller specified
				user = Users.query\
					.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
						Users.RpAccId==rp_acc.RpAccId).first()

			######## generate reg no ########
			try:
				reg_num = generate(UId=user.UId,prefixType='sale_order_invoice_code')
				orderRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
			except:
				# use device model and other info
				orderRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())			

			OInvDesc = req.get('orderDesc')
			orderInv = Order_inv(
					OInvTypeId=2,
					InvStatId=1,
					CurrencyId=1,
					WpId=work_period.WpId,
					RpAccId=rp_acc.RpAccId,
					OInvRegNo=orderRegNo,
					OInvDesc=OInvDesc,
				)
			db.session.add(orderInv)
			OInvTotal = 0
			order_inv_lines = []
			failed_order_inv_lines = []		
			for resElement in req['cartData']:
				ResId = int(req['cartData'][resElement].get('resId'))
				OInvLineAmount = int(req['cartData'][resElement].get('productQty'))

				resource = Resource.query\
					.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
						Resource.ResId==ResId).first()
				res_total = Res_total.query\
					.filter(and_(Res_total.GCRecord=='' or Res_total.GCRecord==None),\
						Res_total.ResId==ResId).first()
				totalSubstitutionResult = totalQtySubstitution(res_total.ResTotBalance,OInvLineAmount)
				try:
					if not resource or totalSubstitutionResult['status']==0:
						raise Exception

					resourceInv = resource.to_json_api()
					OInvLineAmount = totalSubstitutionResult['amount']
					# # !! this shouldn't change total val if order_inv
					# res_total.ResTotBalance = totalSubstitutionResult['totalBalance']
					res_price = Res_price.query\
						.filter(and_(Res_price.GCRecord=='' or Res_price.GCRecord==None),\
							Res_price.ResId==resource.ResId,Res_price.ResPriceTypeId==2).first()
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
					if not 'CurrencyId' in resourceInv:
						resourceInv['CurrencyId'] = 1
					
					order_inv_line = addOInvLineDict(resourceInv)

					# OInvLineRegNo generation
					try:
						reg_num = generate(UId=user.UId,prefixType='order_invoice_line_code')
						orderLineRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
					except:
						# use device model and other info
						orderLineRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
					order_inv_line['OInvLineRegNo']=orderLineRegNo
					
					# increment of Main Order Inv Total Price
					OInvTotal += OInvLineFTotal
					print(order_inv_line)
					thisOInvLine = Order_inv_line(**order_inv_line)
					db.session.add(thisOInvLine)			
					order_inv_lines.append(thisOInvLine.to_json_api())
				except:
					failed_order_inv_lines.append(req['cartData'][resElement])

			if (len(order_inv_lines)==0):
				raise Exception
			###### final order assignment and processing ######
			# add taxes and stuff later on
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,
				current_app.config['PRICE_2_TEXT_LANGUAGE'],
				current_app.config['PRICE_2_TEXT_CURRENCY'])

			orderInv.OInvTotal = decimal.Decimal(OInvTotal)
			orderInv.OInvFTotal = decimal.Decimal(OInvFTotal)
			orderInv.OInvFTotalInWrite = OInvFTotalInWrite

			db.session.commit()

			response = jsonify({
				'status':'added',
				'responseText':gettext('Checkout')+' '+gettext('successfully done')+'! '+gettext('View orders in profile page.')
				})

		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!')
				})
	return response
