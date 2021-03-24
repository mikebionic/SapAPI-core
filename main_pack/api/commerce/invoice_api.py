# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime

from . import api
from main_pack.config import Config
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.api.auth.utils import token_required
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json

from .invoices import save_invoice_request_data, collect_invoice_info


@api.route("/tbl-dk-invoices/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_invoices():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		startDate = request.args.get("startDate",None,type=str)
		endDate = request.args.get("endDate",datetime.now())

		res = collect_invoice_info(
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

		data, fails = save_invoice_request_data(req)
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


@api.route("/tbl-dk-invoices/<InvRegNo>/")
@sha_required
def api_invoice_info(InvRegNo):
	invoice_list = [{"InvRegNo": InvRegNo}]
	res = collect_invoice_info(
		invoice_list = invoice_list,
		single_object = True)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)


# api/v-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-invoices/",methods=['GET'])
@token_required
def api_v_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	current_user = user['current_user']
	res = collect_invoice_info(
		startDate = startDate,
		endDate = endDate,
		rp_acc_user = current_user)

	status_code = 200
	return make_response(jsonify(res), status_code)


@api.route("/v-invoices/<InvRegNo>/",methods=['GET'])
@token_required
def api_v_invoice(user,InvRegNo):
	current_user = user['current_user']
	invoice_list = [{"InvRegNo": InvRegNo}]
	res = collect_invoice_info(
		invoice_list = invoice_list,
		single_object = True,
		rp_acc_user = current_user)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)