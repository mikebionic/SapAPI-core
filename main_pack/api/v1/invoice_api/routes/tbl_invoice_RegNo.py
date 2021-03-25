# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from datetime import datetime

from main_pack.api.v1.invoice_api import api
from main_pack.api.auth.utils import sha_required
from main_pack.api.v1.invoice_api.utils import collect_invoice_data


@api.route("/tbl-invoices/<InvRegNo>/")
@sha_required
def tbl_invoice_RegNo(InvRegNo):
	invoice_list = [{"InvRegNo": InvRegNo}]

	res = collect_invoice_data(
		invoice_list = invoice_list,
		single_object = True
	)

	status_code = 200 if res['status'] == 1 else 404
	return make_response(jsonify(res), status_code)
