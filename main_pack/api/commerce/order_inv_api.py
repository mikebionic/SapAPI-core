from flask import render_template,url_for,jsonify,request,abort,make_response,redirect
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Order_inv,Order_inv_line
from main_pack.api.commerce.utils import addOrderInvDict,addOrderInvLineDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import token_required
from main_pack.api.auth.api_login import sha_required
from sqlalchemy import and_
from main_pack.api.users.utils import apiRpAccData
from main_pack.models.users.models import Rp_acc

@api.route("/tbl-dk-order-invoices/",methods=['GET','POST'])
@sha_required
def api_order_invoices():
	if request.method == 'GET':
		data=[]
		order_invoices = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.InvStatId==1)).all()
		for order_invoice in order_invoices:
			oInvData = order_invoice.to_json_api()
			rp_acc = Rp_acc.query.get(order_invoice.RpAccId)
			if rp_acc:
				rpAccData = apiRpAccData(rp_acc.RpAccRegNo)
				oInvData['Rp_acc'] = rpAccData['data']

			order_inv_lines = Order_inv_line.query\
				.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
					Order_inv_line.OInvId==order_invoice.OInvId).all()

			order_inv_lines_list = []
			for order_inv_line in order_inv_lines:
				order_inv_lines_list.append(order_inv_line.to_json_api())
			oInvData['Order_inv_lines'] = order_inv_lines_list

			data.append(oInvData)
		res = {
			"status":1,
			"message":"All order invoices",
			"data":data,
			"total":len(order_invoices)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			order_invoices = []
			failed_order_invoices = [] 
			for data in req['data']:
				order_invoice = addOrderInvDict(data)
				try:
					OInvRegNo = order_invoice['OInvRegNo']
					thisOrderInv = Order_inv.query\
						.filter(Order_inv.OInvRegNo==OInvRegNo).first()
					if thisOrderInv:
						thisOrderInv.update(**order_invoice)
						db.session.commit()
						print('order invoice updated')
					else:
						newOrderInv = Order_inv(**order_invoice)
						db.session.add(newOrderInv)
						db.session.commit()
						print('order invoice created')

					order_inv_lines = []
					failed_order_inv_lines = []
					print(data['Order_inv_lines'])
					for order_inv_line in data['Order_inv_lines']:
						order_inv_line = addOrderInvLineDict(order_inv_line)
						try:
							OInvLineId = order_inv_line['OInvLineId']
							thisOrderInv = Order_inv_line.query.get(int(OInvLineId))
							if thisOrderInv:
								thisOrderInv.update(**order_inv_line)
								db.session.commit()
								order_inv_lines.append(order_inv_line)
							else:
								newOrderInv = Order_inv_line(**order_inv_line)
								db.session.add(newOrderInv)
								db.session.commit()
								order_inv_lines.append(order_inv_line)
						except:
							failed_order_inv_lines.append(order_inv_line)

					order_invoice['Order_inv_lines'] = order_inv_lines
					order_invoices.append(order_invoice)

				except:
					failed_order_invoices.append(order_invoice)

			status = checkApiResponseStatus(order_invoices,failed_order_invoices)
			res = {
				"data":order_invoices,
				"fails":failed_order_invoices,
				"success_total":len(order_invoices),
				"fail_total":len(failed_order_invoices),
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)

	return response

@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	if model_type=='Rp_acc':
		RpAccId = current_user.RpAccId

		order_invoices = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
				Order_inv.RpAccId==RpAccId).all()

		order_inv_list = []
		for order_inv in order_invoices:
			order_inv_list.append(order_inv.to_json_api())

		res = {
			"data":order_inv_list,
			"total":len(order_inv_list),
			"status":1,
			"message":"Orders"
		}
		response = make_response(jsonify(res),200)
	return response

@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	model_type = user['model_type']
	current_user = user['current_user']

	if model_type=='Rp_acc':
		RpAccId = current_user.RpAccId

		order_invoice = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
				Order_inv.RpAccId==RpAccId,\
				Order_inv.OInvRegNo==OInvRegNo).first()

		order_inv_lines = Order_inv_line.query\
			.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
				Order_inv_line.OInvId==order_invoice.OInvId).all()

		order_invoice = order_invoice.to_json_api()
		order_inv_lines_list = []
		for order_inv_line in order_inv_lines:
			order_inv_lines_list.append(order_inv_line.to_json_api())

		order_invoice['Order_inv_lines'] = order_inv_lines_list
		res = {
			"data":order_invoice,
			"total":len(order_inv_lines_list),
			"status":1,
			"message":"Order lines"
		}
		response = make_response(jsonify(res),200)
	return response