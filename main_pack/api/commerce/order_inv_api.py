# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime

from . import api
from main_pack import db
from main_pack.config import Config

from main_pack.api.auth.utils import token_required
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from .order_invoices import collect_order_invoice_info, save_order_request_data
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

		res = collect_order_invoice_info(
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

		data, fails = save_order_request_data(req)
		status = checkApiResponseStatus(data, fails)

		res = {
			"data": data,
			"fails": fails,
			"success_total": len(data),
			"fail_total": len(fails),
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

	res = collect_order_invoice_info(
		invoice_list = invoice_list,
		show_inv_line_resource = True,
		single_object = True)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)


# Order_invoice of an Rp_acc (@token_required)
# example request:
# api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	current_user = user['current_user']

	res = collect_order_invoice_info(
		startDate = startDate,
		endDate = endDate,
		show_inv_line_resource = True,
		rp_acc_user = current_user)

	status_code = 200
	return make_response(jsonify(res), status_code)


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
	return make_response(jsonify(res), status_code)


@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	current_user = user['current_user']
	invoice_list = [{"OInvRegNo": OInvRegNo}]

	res = collect_order_invoice_info(
		invoice_list = invoice_list,
		single_object = True,
		show_inv_line_resource = True,
		rp_acc_user = current_user)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)