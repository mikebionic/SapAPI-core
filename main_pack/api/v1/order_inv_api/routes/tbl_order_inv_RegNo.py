# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack.api.auth.utils import sha_required

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import collect_order_invoice_data


@api.route("/tbl-order-invoices/<OInvRegNo>/")
@sha_required
def tbl_order_inv_RegNo(OInvRegNo):
	invoice_list = [{"OInvRegNo": OInvRegNo}]

	res = collect_order_invoice_data(
		invoice_list = invoice_list,
		show_inv_line_resource = True,
		single_object = True
	)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)