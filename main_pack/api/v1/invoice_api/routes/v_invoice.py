# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from datetime import datetime

from main_pack.api.v1.invoice_api import api
from main_pack.api.auth.utils import sha_required
from main_pack.api.v1.invoice_api.utils import get_invoices


@api.route("/v-invoices/", methods=["GET", "POST"])
@sha_required
def v_invoice():
	arg_data = {
		"DivId": request.args.get("DivId", None, type=int),
		"notDivId": request.args.get("notDivId", None, type=int),

		"UId": request.args.get("userId", None, type=int),
		"RpAccId": request.args.get("rpAccId", None, type=int),
	}

	if request.method == "POST":
		data = []
		req = request.get_json()
		try:
			arg_data["invoices_to_exclude"] = req if req else None
		except Exception as ex:
			print(f"{datetime.now()} | v-invoices by excluded list Exception {ex}")
		res = get_invoices(**arg_data)

	status_code = 200
	return make_response(jsonify(res), status_code)