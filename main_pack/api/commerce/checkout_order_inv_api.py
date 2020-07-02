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

# @api.route("/test_token/",methods=['GET'])
# @token_required
# def token_test(user):
# 	model_type = user['model_type']
# 	current_user = user['current_user']
# 	if model_type=='Users':
# 		name = current_user.UName
# 	elif model_type=='Rp_acc':
# 		name = current_user.RpAccUName
# 	print(name)
# 	return name

@api.route("/checkout-sale-order-inv/",methods=['POST'])
@token_required
def api_checkout_sale_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']
	# if model_type=='Users':
	# 	name = current_user.UName
	if model_type=='Rp_acc':
		name = current_user.RpAccUName
		RpAccId = current_user.RpAccId
		user = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.RpAccId==RpAccId).first()

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
	
	order_inv_lines = []
	failed_order_inv_lines = []
	OInvTotal = 0
	OrderInvLines = req['orderInv']['OrderInvLines']
	for order_inv_line_req in OrderInvLines:
		order_inv_line = addOrderInvLineDict(order_inv_line_req)
		print('invoice line incoming data')
		print(order_inv_line)
		print('--------------------')

		ResId = order_inv_line['ResId']
		OInvLineAmount = int(order_inv_line['OInvLineAmount'])
		resource = Resource.query\
			.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
				Resource.ResId==ResId).first()
		print(resource.to_json_api())
		res_total = Res_total.query\
			.filter(and_(Res_total.GCRecord=='' or Res_total.GCRecord==None),\
				Res_total.ResId==ResId).first()
		totalSubstitutionResult = totalQtySubstitution(res_total.ResTotBalance,OInvLineAmount)
		if not resource or totalSubstitutionResult['status']==0:
			failed_order_inv_lines.append(order_inv_line_req)
		else:
			try:
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
				db.session.add(thisOInvLine)			
				order_inv_lines.append(thisOInvLine.to_json_api())
			except:
				print(Exception.message)
				failed_order_inv_lines.append()

	# add taxes and stuff later on
	OInvFTotal = OInvTotal
	OInvFTotalInWrite = price2text(OInvFTotal,
		current_app.config['PRICE_2_TEXT_LANGUAGE'],
		current_app.config['PRICE_2_TEXT_CURRENCY'])

	newOrderInv.OInvTotal = OInvTotal
	newOrderInv.OInvFTotal = OInvFTotal
	newOrderInv.OInvFTotalInWrite = OInvFTotalInWrite

	print(newOrderInv.to_json_api())

	db.session.commit()

	status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)
	res = {
		"data":order_inv_lines,
		"fails":failed_order_inv_lines,
		"success_total":len(order_inv_lines),
		"fail_total":len(failed_order_inv_lines)
	}

	for e in status:
		res[e]=status[e]
	response = make_response(jsonify(res),200)

	return response