# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack.api.auth.utils import token_required

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import collect_order_inv_data


@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def v_order_inv_RegNo(user,OInvRegNo):
	currency_code = request.args.get("currency",None,type=str)

	current_user = user['current_user']
	invoice_list = [{"OInvRegNo": OInvRegNo}]

	res = collect_order_inv_data(
		invoice_list = invoice_list,
		single_object = True,
		show_inv_line_resource = True,
		rp_acc_user = current_user,
		currency_code = currency_code.upper() if currency_code else None,
	)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)