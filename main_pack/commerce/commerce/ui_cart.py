from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

from main_pack.commerce.commerce.cart_utils import UiCartResourceData
from main_pack.models.commerce.models import Resource,Order_inv,Order_inv_line
from main_pack.commerce.commerce.order_utils import addOInvLineDict,addOInvDict

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNum,generate,validate
from main_pack.base.num2text import num2text,price2text

@bp.route("/product/ui_cart/", methods=['POST','PUT'])
def ui_cart():
	product_list=[]
	if request.method == "POST":
		try:
			req = request.get_json()
			resId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['resId'] = resId
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
				resId = req[resElement].get('resId')
				productQty = req[resElement].get('productQty')
				
				product={}
				product['resId'] = resId
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
			resId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['resId'] = resId
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
				resId = req[resElement].get('resId')
				productQty = req[resElement].get('productQty')
				
				product={}
				product['resId'] = resId
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



# {
# 	'product6':{
# 		'resId': '6',
# 		'priceValue': '11.0',
# 		'productQty': 5
# 	},
# 	'product5':{
# 		'resId': '5',
# 		'priceValue': '9.5',
# 		'productQty': 1
# 	},
# 	'product8':{
# 		'resId': '8',
# 		'priceValue': '10.0',
# 		'productQty': 1
# 	}
# }

@bp.route("/product/ui_cart_checkout/", methods=['POST'])
def ui_cart_checkout():
	if request.method == "POST":
		req = request.get_json()
		try:
			reg_num = generate(UId=current_user.UId,prefixType='sale order invoice code')
			try:
				regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			except:
				print("err generating regNo")

			orderInv = Order_inv(
					OInvTypeId=2,InvStatId=1,CurrencyId=1,
					RpAccId=current_user.RpAccId,
					OInvRegNo=regNo
				)
			db.session.add(orderInv)
			OInvTotal = 0
			for resElement in req:
				resId = req[resElement].get('resId')
				productQty = int(req[resElement].get('productQty'))
				priceValue = float(req[resElement].get('priceValue'))
				resource = Resource.query.get(resId)
				resourceInv = resource.to_json_api()
				priceTotal = priceValue*productQty
				priceFTotal = priceTotal
				resourceInv['OInvLineAmount'] = productQty
				resourceInv['OInvLinePrice'] = priceValue
				resourceInv['OInvLineTotal'] = priceTotal
				resourceInv['OInvLineFTotal'] = priceFTotal
				resourceInv['OInvId'] = orderInv.OInvId
				resourceInv['CurrencyId'] = 1
				print("Order inv id is "+str(resourceInv['OInvId']))
				
				order_inv_line = addOInvLineDict(resourceInv)
				
				OInvTotal += priceFTotal
				thisOInvLine = Order_inv_line(**order_inv_line)
				db.session.add(thisOInvLine)

			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,'tk','TMT')

			orderInv.OInvTotal = OInvTotal
			orderInv.OInvFTotal = OInvFTotal
			orderInv.OInvFTotalInWrite = OInvFTotalInWrite

			db.session.commit()

			response = jsonify({
				'status':'added',
				'responseText':gettext('Checkout')+' '+gettext('successfully done!'),
				'htmlData':render_template('commerce/main/commerce/successCheckoutAppend.html')
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response
