# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.api.v1.device_api import api
from main_pack.api.v1.device_api.utils import save_device_sync_data


@api.route("/tbl-devices/", methods=['POST'])
@sha_required
@request_is_json(request)
def tbl_device_post():
	req = request.get_json()

	data, fails = save_device_sync_data(req)
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