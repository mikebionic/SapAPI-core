# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack.api.auth.utils import admin_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.warehouse_api import api
from main_pack.api.v1.warehouse_api.utils import save_warehouse_synch_data


@api.post("/tbl-dk-warehouses/")
@admin_required
@request_is_json(request)
def tbl_warehouse_post(user):

	req = request.get_json()
	data, fails = save_warehouse_synch_data(req)
	status = checkApiResponseStatus(data, fails)

	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)