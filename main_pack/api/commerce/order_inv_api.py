# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack import db

# orders and db methods
from main_pack.models.commerce.models import (Order_inv,Resource,
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
from main_pack.api.commerce.pagination_utils import collect_order_inv_paginate_info


@api.route("/tbl-dk-order-invoices/",methods=['GET','POST'])
@sha_required
def api_order_invoices():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		startDate = request.args.get("startDate",None,type=str)
		endDate = request.args.get("endDate",datetime.now())
		res = apiOrderInvInfo(
			startDate = startDate,
			endDate = endDate,
			statusId = 1,
			DivId = DivId,
			notDivId = notDivId)
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
			for order_inv_req in req:
				order_invoice = addOrderInvDict(order_inv_req)
				try:
					DivGuid = order_invoice_req['DivGuid']
					RpAccGuid = order_invoice_req['RpAccGuid']
					WhGuid = order_invoice_req['WhGuid']
					OInvGuid = order_invoice['OInvGuid']
					OInvRegNo = order_invoice['OInvRegNo']
					order_inv_query = db.session.query(Order_inv, Division, Warehouse, Rp_acc).query\
						.filter_by(OInvGuid = OInvGuid)\
						.outerjoin(Division, Division.DivGuid == DivGuid)\
						.outerjoin(Warehouse, Warehouse.WhGuid == WhGuid)\
						.outerjoin(Rp_acc, Rp_acc.RpAccGuid == RpAccGuid)\
						.first()
					order_invoice['DivId'] = order_inv_query.Division.DivId
					order_invoice['WhId'] = order_inv_query.Warehouse.WhId
					# ??? !!! add "or not Warehouse or not Division" ?
					if not order_inv_query.Rp_acc:
						raise Exception
					order_invoice['RpAccId'] = order_inv_query.Rp_acc.RpAccId

					thisInvStatus = None
					thisOrderInv = order_inv_query.Order_inv
					if thisOrderInv:
						order_invoice['OInvId'] = thisOrderInv.OInvId
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
					for order_inv_line_req in order_inv_req['Order_inv_lines']:
						order_inv_line = addOrderInvLineDict(order_inv_line_req)
						order_inv_line['OInvId'] = thisOrderInv.OInvId
						ResRegNo = order_inv_line_req['ResRegNo']
						this_line_resource = Resources.query.filter_by(ResRegNo = ResRegNo).first() 
						try:
							order_inv_line["ResId"] = this_line_resource.ResId
							OInvLineGuid = order_inv_line['OInvLineGuid']
							thisOrderInvLine = Order_inv_line.query\
								.filter_by(OInvLineGuid = OInvLineGuid)\
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
										print(f"{datetime.now()} | OInv Api Res_total Exception: {ex}")
								db.session.commit()
								order_inv_lines.append(order_inv_line)
							else:
								newOrderInvLine = Order_inv_line(**order_inv_line)
								db.session.add(newOrderInvLine)
								db.session.commit()
								order_inv_lines.append(order_inv_line)
								newOrderInvLine = None
						except Exception as ex:
							print(f"{datetime.now()} | OInv Api OInvLine Exception: {ex}")
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
	res = apiOrderInvInfo(
		invoice_list = invoice_list,
		single_object = True)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


# Order_invoice of an Rp_acc (@token_required)
# example request:
# api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	model_type = user['model_type']
	current_user = user['current_user']
	res = apiOrderInvInfo(
		startDate = startDate,
		endDate = endDate,
		rp_acc_user = current_user)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/v-order-invoices/paginate/",methods=['GET'])
@token_required
def api_v_order_invoices_paginate(user):
	model_type = user['model_type']
	current_user = user['current_user']
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	page = request.args.get("page",1,type=int)
	per_page = request.args.get("per_page",None,type=int)
	sort = request.args.get("sort","date_new",type=str)
	invoices_only = request.args.get("invoices_only",1,type=int)
	invStatus = request.args.get("invStatus",1,type=int)
	pagination_url = 'commerce_api.api_v_order_invoices_paginate'

	res = collect_order_inv_paginate_info(
		pagination_url,
		startDate = startDate,
		endDate = endDate,
		invStatus = invStatus,
		rp_acc_user = current_user,
		DivId = DivId,
		notDivId = notDivId,
		page = page,
		per_page = per_page,
		sort = sort,
		invoices_only = invoices_only)

	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	model_type = user['model_type']
	current_user = user['current_user']
	invoice_list = [{"OInvRegNo": OInvRegNo}]
	res = apiOrderInvInfo(
		invoice_list = invoice_list,
		single_object = True,
		rp_acc_user = current_user)
	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)
	return response