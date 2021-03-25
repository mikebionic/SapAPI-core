# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime

from main_pack.api.auth.utils import token_required

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import collect_order_invoice_data

@api.route("/v-order-invoices/paginate/")
@token_required
def v_order_inv_paginate(user):
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

	res = collect_order_invoice_data(
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