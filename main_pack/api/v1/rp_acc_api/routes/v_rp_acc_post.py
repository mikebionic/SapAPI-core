# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify, abort

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.api.v1.rp_acc_api import api
from main_pack.api.v1.rp_acc_api.utils import save_rp_acc_req_data


@api.route("/v-rp-accs/", methods=['POST'])
@token_required
@request_is_json(request)
def v_rp_acc_post(user):
	model_type = user['model_type']
	current_user = user['current_user']
	if (model_type != "user" or model_type != "device"):
		abort(400)

	req = request.get_json()
	data, fails = save_rp_acc_req_data(req, model_type, current_user)
	status = checkApiResponseStatus(data, fails)

	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails),
		"message": "Rp_acc management"
	}

	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)