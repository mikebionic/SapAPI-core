# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.invoice_api import api
from main_pack.api.v1.invoice_api.utils import save_invoice_synch_data

from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus


@api.route("/tbl-invoices/", methods=['POST'])
@sha_required
@request_is_json(request)
def tbl_invoice_post():
	req = request.get_json()

	data, fails = save_invoice_synch_data(req)
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
	return make_response(jsonify(res), status_code)