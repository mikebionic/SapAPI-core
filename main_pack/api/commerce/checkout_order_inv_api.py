from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.users.models import Users
from main_pack.models.commerce.models import Order_inv,Order_inv_line
from main_pack.api.commerce.utils import addOrderInvDict,addOrderInvLineDict
from main_pack import db,babel,gettext,lazy_gettext
from flask import current_app
from datetime import datetime
from main_pack.api.auth.api_login import token_required

from main_pack.models.commerce.models import Resource,Res_price,Res_total
from main_pack.api.commerce.checkout_utils import totalQtySubstitution
from main_pack.base.num2text import num2text,price2text
from sqlalchemy import and_
from main_pack.key_generator.utils import generate,makeRegNum

# @api.route("/checkout-order-invoices/",methods=['POST'])
# def api_checkout_order_invoices():
# 	if request.method == 'POST':
# 		if not request.json:
# 			res = {
# 				"status": 0,
# 				"message": "Error. Not a JSON data."
# 			}
# 			response = make_response(jsonify(res),400)
			
# 		else:
# 			req = request.get_json()
# 			order_invoices = []
# 			failed_order_invoices = []
# 			order_invoice = addOrderInvDict(req['orderInv'])
# 			print('invoice incoming data')
# 			print(order_invoice)
# 			print('--------------------')
# 			try:
# 				if not 'OInvId' in order_invoice:
# 					newOrderInv = Order_inv(**order_invoice)
# 					db.session.add(newOrderInv)
# 					db.session.commit()
# 					order_invoices.append(order_invoice)
# 				else:
# 					OInvId = order_invoice['OInvId']
# 					thisOrderInv = Order_inv.query.get(int(OInvId))
# 					if thisOrderInv is not None:
# 						thisOrderInv.update(**order_invoice)
# 						db.session.commit()
# 						order_invoices.append(order_invoice)

# 					else:
# 						newOrderInv = Order_inv(**order_invoice)
# 						db.session.add(newOrderInv)
# 						db.session.commit()
# 						order_invoices.append(order_invoice)

# 				order_inv_lines = []
# 				failed_order_inv_lines = [] 
# 				for order_inv_line_req in req['orderInv']['OrderInvLines']:
# 					order_inv_line = addOrderInvLineDict(order_inv_line_req)
# 					print('invoice line incoming data')
# 					print(order_inv_line)
# 					print('--------------------')
# 					try:
# 						if not 'OInvLineId' in order_inv_line:
# 							newOrderInv = Order_inv_line(**order_inv_line)
# 							db.session.add(newOrderInv)
# 							db.session.commit()
# 							order_inv_lines.append(order_inv_line)
# 						else:
# 							OInvLineId = order_inv_line['OInvLineId']
# 							thisOrderInv = Order_inv_line.query.get(int(OInvLineId))
# 							if thisOrderInv is not None:
# 								thisOrderInv.update(**order_inv_line)
# 								db.session.commit()
# 								order_inv_lines.append(order_inv_line)

# 							else:
# 								newOrderInv = Order_inv_line(**order_inv_line)
# 								db.session.add(newOrderInv)
# 								db.session.commit()
# 								order_inv_lines.append(order_inv_line)
# 					except:
# 						failed_order_inv_lines.append(order_inv_line)

# 			except:
# 				print(Exception)
# 				failed_order_invoices.append(order_invoice)

# 			status = checkApiResponseStatus(order_invoices,failed_order_invoices)
# 			res = {
# 				"data":order_invoices[0] if len(order_invoices)==1 else order_invoices,
# 				"fails":failed_order_invoices[0] if len(failed_order_invoices)==1 else failed_order_invoices,
# 				"success_total":len(order_invoices),
# 				"fail_total":len(failed_order_invoices)
# 			}
# 			for e in status:
# 				res[e]=status[e]
# 			response = make_response(jsonify(res),200)
# 			print(response)

# 	return response

@api.route("/test_token/",methods=['GET'])
@token_required
def token_test(user):
	model_type = user['model_type']
	current_user = user['current_user']
	if model_type=='Users':
		name = current_user.UName
	elif model_type=='Rp_acc':
		name = current_user.RpAccUName
	print(name)
	return name

@api.route("/checkout-order-invoices/",methods=['POST'])
@token_required
def api_checkout_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']
	# if model_type=='Users':
	# 	name = current_user.UName
	if model_type=='Rp_acc':
		name = current_user.RpAccUName
		RpAccId = current_user.RpAccId
		user = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.RpAccId==RpAccId).first()

	# try:
	req = request.get_json()

	order_invoice = addOrderInvDict(req['orderInv'])
	print('invoice incoming data')
	print(order_invoice)
	print('--------------------')

	try:
		reg_num = generate(UId=user.UId,prefixType='sale order invoice code')
		orderRegNo = makeRegNum(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
	except:
		# use device model and other info
		orderRegNo = datetime.now()

	print(orderRegNo)
	print('-----------')
	order_invoice['OInvRegNo']=orderRegNo
	order_invoice['InvStatId']=1
	if not order_invoice['CurrencyId']:
		order_invoice['CurrencyId']=1
	order_invoice['RpAccId']=RpAccId

	newOrderInv = Order_inv(**order_invoice)
	db.session.add(newOrderInv)

	OInvTotal = 0
	OrderInvLines = req['orderInv']['OrderInvLines']
	for order_inv_line_req in OrderInvLines:
		order_inv_line = addOrderInvLineDict(order_inv_line_req)
		print('invoice line incoming data')
		print(order_inv_line)
		print('--------------------')

		ResId = order_inv_line['ResId']
		print('resId is '+ str(ResId))
		OInvLineAmount = int(order_inv_line['OInvLineAmount'])
		resource = Resource.query\
			.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
				Resource.ResId==ResId).first()
		print(resource.to_json_api())
		res_total = Res_total.query\
			.filter(and_(Res_total.GCRecord=='' or Res_total.GCRecord==None),\
				Res_total.ResId==ResId).first()
		print(res_total.ResTotBalance)
		print(OInvLineAmount)
		totalSubstitutionResult = totalQtySubstitution(res_total.ResTotBalance,OInvLineAmount)
		print(totalSubstitutionResult)
		if not resource or totalSubstitutionResult['status']==0:
			print('error no resource or status is 0')			
			print('------------')
		else:
			OInvLineAmount = totalSubstitutionResult['amount']
			res_total.ResTotBalance = totalSubstitutionResult['totalBalance']
			# do I need to commit changes here?
			res_price = Res_price.query\
				.filter(and_(Res_price.GCRecord=='' or Res_price.GCRecord==None),\
					Res_price.ResId==resource.ResId).first()
			OInvLinePrice = float(res_price.ResPriceValue) if res_price else 0
			OInvLineTotal = OInvLinePrice*OInvLineAmount
			# add taxes and stuff later on
			OInvLineFTotal = OInvLineTotal
			####--------------####
			order_inv_line['OInvLinePrice'] = OInvLinePrice
			order_inv_line['OInvLineTotal'] = OInvLineTotal
			order_inv_line['OInvLineFTotal'] = OInvLineFTotal
			order_inv_line['OInvId'] = newOrderInv.OInvId
			if not order_inv_line['CurrencyId']:
				order_inv_line['CurrencyId'] = 1
			
			# increment of Main Order Inv Total Price
			OInvTotal += OInvLineFTotal

		thisOInvLine = Order_inv_line(**order_inv_line)
		# db.session.add(thisOInvLine)
		print(thisOInvLine)

	# add taxes and stuff later on
	OInvFTotal = OInvTotal
	OInvFTotalInWrite = price2text(OInvFTotal,
		current_app.config['PRICE_2_TEXT_LANGUAGE'],
		current_app.config['PRICE_2_TEXT_CURRENCY'])

	newOrderInv.OInvTotal = OInvTotal
	newOrderInv.OInvFTotal = OInvFTotal
	newOrderInv.OInvFTotalInWrite = OInvFTotalInWrite

	print(newOrderInv.to_json_api())

	# db.session.commit()

	response = jsonify({
		'status':'added',
		'responseText':gettext('Checkout')+' '+gettext('successfully done!'),
		# 'htmlData':render_template('commerce/main/commerce/successCheckoutAppend.html')
		})
	# except:
	# 	print(Exception)
	# 	response = jsonify({
	# 		'status':'error',
	# 		'responseText':gettext('Unknown error!'),
	# 		})
	return response