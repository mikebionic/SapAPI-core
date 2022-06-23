# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from datetime import datetime

from main_pack.api.v1.invoice_api import api
from main_pack.api.auth.utils import token_required
from main_pack.api.v1.invoice_api.utils import collect_invoice_data


@api.route("/v-invoices/")
@token_required
def v_invoice(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	current_user = user['current_user']

	res = collect_invoice_data(
		startDate = startDate,
		endDate = endDate,
		rp_acc_user = current_user
	)

	status_code = 200
	return make_response(jsonify(res), status_code)