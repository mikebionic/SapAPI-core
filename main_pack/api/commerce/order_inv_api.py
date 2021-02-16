# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from sqlalchemy import and_, extract

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /

from . import api
from main_pack import db
from main_pack.config import Config

# orders and db methods
from main_pack.models.commerce.models import (
	Order_inv,Resource,
	Order_inv_line,
	Inv_status,
	Res_total
)
from .utils import (
	addOrderInvDict,
	addOrderInvLineDict
)
from main_pack.models.base.models import Warehouse, Division
from main_pack.base.apiMethods import checkApiResponseStatus
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models.users.models import Rp_acc
# / Rp_acc db Model and methods /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# auth and validation
from main_pack.api.auth.utils import token_required
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
# / auth and validation /

from .commerce_utils import apiOrderInvInfo
from .pagination_utils import collect_order_inv_paginate_info


@api.route("/tbl-dk-order-invoices/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
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
			notDivId = notDivId,
			currency_code = Config.MAIN_CURRENCY_CODE)
	
		status_code = 200
		response = make_response(jsonify(res), status_code)

	elif request.method == 'POST':

		req = request.get_json()

		divisions = Division.query\
			.filter_by(GCRecord = None)\
			.filter(Division.DivGuid != None).all()
		warehouses = Warehouse.query\
			.filter_by(GCRecord = None)\
			.filter(Warehouse.WhGuid != None).all()
		rp_accs = Rp_acc.query\
			.filter_by(GCRecord = None)\
			.filter(Rp_acc.RpAccGuid != None).all()

		division_DivId_list = [division.DivId for division in divisions]
		division_DivGuid_list = [str(division.DivGuid) for division in divisions]

		warehouse_WhId_list = [warehouse.WhId for warehouse in warehouses]
		warehouse_WhGuid_list = [str(warehouse.WhGuid) for warehouse in warehouses]

		rp_acc_RpAccId_list = [rp_acc.RpAccId for rp_acc in rp_accs]
		rp_acc_RpAccGuid_list = [str(rp_acc.RpAccGuid) for rp_acc in rp_accs]
		
		data = []
		failed_data = [] 

		for order_inv_req in req:
			try:
				order_invoice = addOrderInvDict(order_inv_req)
				DivGuid = order_inv_req['DivGuid']
				WhGuid = order_inv_req['WhGuid']
				RpAccGuid = order_inv_req['RpAccGuid']
				RpAccRegNo = order_inv_req['RpAccRegNo']

				OInvGuid = order_invoice['OInvGuid']
				OInvRegNo = order_invoice['OInvRegNo']

				try:
					indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
					DivId = int(indexed_div_id)
				except:
					DivId = None
				try:
					indexed_wh_id = warehouse_WhId_list[warehouse_WhGuid_list.index(WhGuid)]
					WhId = int(indexed_wh_id)
				except:
					WhId = None
				try:
					indexed_rp_acc_id = rp_acc_RpAccId_list[rp_acc_RpAccGuid_list.index(RpAccGuid)]
					RpAccId = int(indexed_rp_acc_id)
				except:
					RpAccId = None

				order_invoice['DivId'] = DivId
				order_invoice['WhId'] = WhId
				order_invoice['RpAccId'] = RpAccId

				thisOrderInv = Order_inv.query\
					.filter_by(
						OInvGuid = OInvGuid,
						OInvRegNo = OInvRegNo,
						GCRecord = None)\
					.first()
				thisInvStatus = None

				if not RpAccId or not DivId or not WhId:
					print(f"{RpAccId}, {DivId}, {WhId}")
					raise Exception

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
					ResGuid = order_inv_line_req['ResGuid']

					this_line_resource = Resources.query\
						.filter_by(
							ResRegNo = ResRegNo,
							ResGuid = ResGuid,
							GCRecord = None)\
						.first() 

					try:
						order_inv_line["ResId"] = this_line_resource.ResId
						OInvLineRegNo = order_inv_line['OInvLineRegNo']
						OInvLineGuid = order_inv_line['OInvLineGuid']

						thisOrderInvLine = Order_inv_line.query\
							.filter_by(
								OInvLineRegNo = OInvLineRegNo,
								OInvLineGuid = OInvLineGuid,
								GCRecord = None)\
							.first()

						if thisOrderInvLine:
							order_inv_line["OInvLineId"] = thisOrderInvLine.OInvLineId
							thisOrderInvLine.update(**order_inv_line)
							if thisInvStatus == 9 or thisInvStatus == 5:
								try:
									if (old_invoice_status != 5 or old_invoice_status != 9):
										order_res_total = Res_total.query\
											.filter_by(
												ResId = thisOrderInvLine.ResId,
												GCRecord = None)\
											.first()
										order_res_total.ResPendingTotalAmount += thisOrderInvLine.OInvLineAmount

								except Exception as ex:
									print(f"{datetime.now()} | OInv Api Res_total Exception: {ex}")

							db.session.commit()
							order_inv_lines.append(order_inv_line_req)

						else:
							thisOrderInvLine = Order_inv_line(**order_inv_line)
							db.session.add(thisOrderInvLine)
							db.session.commit()
							order_inv_lines.append(order_inv_line_req)
							thisOrderInvLine = None

					except Exception as ex:
						print(f"{datetime.now()} | OInv Api OInvLine Exception: {ex}")
						failed_order_inv_lines.append(order_inv_line_req)

				order_invoice['Order_inv_lines'] = order_inv_lines
				data.append(order_invoice)

			except Exception as ex:
				print(f"{datetime.now()} | OInv Api Exception: {ex}")
				failed_data.append(order_invoice)

		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data),
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response


@api.route("/tbl-dk-order-invoices/<OInvRegNo>/")
@sha_required
def api_order_invoice_info(OInvRegNo):
	invoice_list = [{"OInvRegNo": OInvRegNo}]

	res = apiOrderInvInfo(
		invoice_list = invoice_list,
		single_object = True)

	status_code = 200
	response = make_response(jsonify(res), status_code)
	return response


# Order_invoice of an Rp_acc (@token_required)
# example request:
# api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	current_user = user['current_user']

	res = apiOrderInvInfo(
		startDate = startDate,
		endDate = endDate,
		show_inv_line_resource = True,
		rp_acc_user = current_user)

	status_code = 200
	response = make_response(jsonify(res), status_code)
	return response


@api.route("/v-order-invoices/paginate/",methods=['GET'])
@token_required
def api_v_order_invoices_paginate(user):
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
	response = make_response(jsonify(res), status_code)
	return response


@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	current_user = user['current_user']
	invoice_list = [{"OInvRegNo": OInvRegNo}]

	res = apiOrderInvInfo(
		invoice_list = invoice_list,
		single_object = True,
		show_inv_line_resource = True,
		rp_acc_user = current_user)

	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404

	response = make_response(jsonify(res), status_code)
	return response