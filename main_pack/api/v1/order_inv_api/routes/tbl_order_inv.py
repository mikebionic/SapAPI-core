# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime

from main_pack.config import Config
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import collect_order_inv_data


@api.route("/tbl-order-invoices/", methods=['GET'])
@sha_required
@request_is_json(request)
def tbl_order_inv():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())

	res = collect_order_inv_data(
		startDate = startDate,
		endDate = endDate,
		statusId = 1,
		DivId = DivId,
		notDivId = notDivId,
		currency_code = Config.MAIN_CURRENCY_CODE
	)

	status_code = 200
	return make_response(jsonify(res), status_code)