# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime

from main_pack.api.auth.utils import token_required

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import collect_order_inv_data


@api.route("/v-order-invoices/")
@token_required
def v_order_inv(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	statusId = request.args.get("statusId",None,type=int)
	currency_code = request.args.get("currency",None,type=str)

	current_user = user['current_user']

	res = collect_order_inv_data(
		startDate = startDate,
		endDate = endDate,
		statusId = statusId,
		show_inv_line_resource = True,
		rp_acc_user = current_user,
		currency_code = currency_code.upper() if currency_code else None,
	)

	status_code = 200
	return make_response(jsonify(res), status_code)