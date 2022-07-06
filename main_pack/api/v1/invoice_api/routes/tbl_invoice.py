# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from datetime import datetime

from main_pack.config import Config
from main_pack.api.v1.invoice_api import api
from main_pack.api.v1.invoice_api.utils import collect_invoice_data
from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json


@api.route("/tbl-invoices/")
@admin_required
def tbl_invoice_get(user):
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())

	res = collect_invoice_data(
		startDate = startDate,
		endDate = endDate,
		statusId = 1,
		DivId = DivId,
		notDivId = notDivId,
		currency_code = Config.MAIN_CURRENCY_CODE)

	status_code = 200
	return make_response(jsonify(res), status_code)