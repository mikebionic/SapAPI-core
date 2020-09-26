# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack import db

# orders and db methods
from main_pack.models.commerce.models import (Order_inv,
																							Order_inv_line,
																							Inv_status,
																							Res_total)
from main_pack.api.commerce.utils import (addOrderInvDict,
																					addOrderInvLineDict)
from main_pack.base.apiMethods import checkApiResponseStatus
from sqlalchemy import and_, extract
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models.users.models import Rp_acc
from main_pack.api.users.utils import apiRpAccData
# / Rp_acc db Model and methods /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# auth and validation
from main_pack.api.auth.api_login import token_required
from main_pack.api.auth.api_login import sha_required
# / auth and validation /

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /

from main_pack.api.commerce.commerce_utils import apiOrderInvInfo


@api.route("/tbl-dk-order-invoices/",methods=['GET','POST'])
@sha_required
def api_order_invoices():
	if request.method == 'GET':
		startDate = request.args.get("startDate",None,type=str)
		endDate = request.args.get("endDate",datetime.now())
		res = apiOrderInvInfo(startDate,
													endDate,
													statusId=1)
		status_code = 200
		response = make_response(jsonify(res),status_code)
		return response

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
			for data in req:
				order_invoice = addOrderInvDict(data)
				try:
					OInvRegNo = order_invoice['OInvRegNo']
					thisOrderInv = Order_inv.query.filter_by(OInvRegNo = OInvRegNo).first()
					# getting correct rp_acc of a database
					try:
						RpAccRegNo = data['Rp_acc']['RpAccRegNo']
						RpAccName = data['Rp_acc']['RpAccName']
						rp_acc = Rp_acc.query\
							.filter_by(RpAccRegNo = RpAccRegNo, RpAccName = RpAccName)\
							.first()
						if rp_acc:
							order_invoice['RpAccId'] = rp_acc.RpAccId
					except Exception as ex:
						print(f"{datetime.now()} | OInv Api Exception: {ex}")
						print("Rp_acc not provided")
						abort(400)

					thisInvStatus = None

					if thisOrderInv:
						old_invoice_status = thisOrderInv.InvStatId
						thisOrderInv.update(**order_invoice)
						db.session.commit()
						# if status: "returned" or "cancelled" (id=9, id=5) 
						# all lines should update 
						# res_total.ResPendingTotalAmount
						thisInvStatus = thisOrderInv.InvStatId

					else:
						thisOrderInv = Order_inv(**order_invoice)
						db.session.add(thisOrderInv)
						db.session.commit()

					order_inv_lines = []
					failed_order_inv_lines = []
					for order_inv_line in data['Order_inv_lines']:
						order_inv_line = addOrderInvLineDict(order_inv_line)
						order_inv_line['OInvId'] = thisOrderInv.OInvId
						try:
							OInvLineRegNo = order_inv_line['OInvLineRegNo']
							thisOrderInvLine = Order_inv_line.query\
								.filter_by(OInvLineRegNo = OInvLineRegNo)\
								.first()
							if thisOrderInvLine:
								thisOrderInvLine.update(**order_inv_line)
								if thisInvStatus == 9 or thisInvStatus == 5:
									try:
										if (old_invoice_status != 5 or old_invoice_status != 9):
											order_res_total = Res_total.query\
												.filter_by(ResId = thisOrderInvLine.ResId)\
												.first()
											order_res_total.ResPendingTotalAmount += thisOrderInvLine.OInvLineAmount
									except Exception as ex:
										print(f"{datetime.now()} | OInv Api Exception: {ex}")
								db.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line updated')
							else:
								newOrderInvLine = Order_inv_line(**order_inv_line)
								db.session.add(newOrderInvLine)
								db.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line created')
						except Exception as ex:
							print(f"{datetime.now()} | OInv Api Exception: {ex}")
							failed_order_inv_lines.append(order_inv_line)

					order_invoice['Order_inv_lines'] = order_inv_lines
					order_invoices.append(order_invoice)

				except Exception as ex:
					print(f"{datetime.now()} | OInv Api Exception: {ex}")
					failed_order_invoices.append(order_invoice)

			status = checkApiResponseStatus(order_invoices,failed_order_invoices)
			res = {
				"data": order_invoices,
				"fails": failed_order_invoices,
				"success_total": len(order_invoices),
				"fail_total": len(failed_order_invoices),
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)

	return response


@api.route("/tbl-dk-order-invoices/<OInvRegNo>/")
@sha_required
def api_order_invoice_info(OInvRegNo):
	invoice_list = [{"OInvRegNo": OInvRegNo}]
	res = apiOrderInvInfo(invoice_list=invoice_list,
												single_object=True)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


# example request:
# api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	model_type = user['model_type']
	current_user = user['current_user']
	res = apiOrderInvInfo(startDate=startDate,
												endDate=endDate,
												rp_acc_user=current_user)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	model_type = user['model_type']
	current_user = user['current_user']
	invoice_list = [{"OInvRegNo": OInvRegNo}]
	res = apiOrderInvInfo(invoice_list=invoice_list,
												single_object=True,
												rp_acc_user=current_user)
	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)
	return response
