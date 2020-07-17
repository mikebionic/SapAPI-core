from flask import render_template,url_for,jsonify,json,session,flash,redirect,request,Response,abort
from flask import current_app
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from sqlalchemy import and_

from main_pack.commerce.commerce.cart_utils import UiCartResourceData
from main_pack.models.commerce.models import Resource,Order_inv,Order_inv_line
from main_pack.commerce.commerce.order_utils import addOInvLineDict,addOInvDict

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.models.commerce.models import Res_price,Res_total
from main_pack.base.invoiceMethods import totalQtySubstitution
from main_pack.key_generator.utils import makeRegNum,generate,validate
from main_pack.base.num2text import num2text,price2text
from datetime import datetime
import decimal
from main_pack.models.users.models import Users,Rp_acc

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

			# get the rp_acc of current logged user
			rp_acc = Rp_acc.query\
				.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
					Rp_acc.RpAccId==current_user.RpAccId).first()
			try:
				# get the seller user of the rp_acc
				Rp_acc_user = Users.query\
					.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
						Users.RpAccId==rp_acc.RpAccId).first()
				if Rp_acc_user:
					reg_num = generate(UId=Rp_acc_user.UId,prefixType='sale order invoice code')
					regNo = makeRegNum(Rp_acc_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
				else:
					# else if no seller user found for a current rp_acc:
					reg_num = generate(UId=current_user.UId,prefixType='sale order invoice code')
					regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
			except:
				regNo = datetime.now()
			
			OInvDesc = req.get('orderDesc')
			orderInv = Order_inv(
					OInvTypeId=2,
					InvStatId=1,
					CurrencyId=1,
					RpAccId=rp_acc.RpAccId,
					OInvRegNo=regNo,
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
