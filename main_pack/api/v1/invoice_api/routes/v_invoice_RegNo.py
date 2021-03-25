# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from datetime import datetime

from main_pack.api.v1.invoice_api import api
from main_pack.api.auth.utils import token_required
from main_pack.api.v1.invoice_api.utils import collect_invoice_data


@api.route("/v-invoices/<InvRegNo>/")
@token_required
def v_invoice_RegNo(user, InvRegNo):
	current_user = user['current_user']
	invoice_list = [{"InvRegNo": InvRegNo}]

	res = collect_invoice_data(
		invoice_list = invoice_list,
		single_object = True,
		rp_acc_user = current_user
	)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)