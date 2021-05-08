# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify, abort

from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.rp_acc_api import api
from main_pack.api.v1.rp_acc_api.utils import check_Rp_acc_existence


@api.route("/check-rp-acc-existence/", methods=['POST'])
@request_is_json(request)
def check_rp_acc_existence():

	req = request.get_json()
	data = check_Rp_acc_existence(req)

	res = {
		"data": data,
		"status": 1 if data else 0,
		"total": 1 if data else 0,
		"message": "check Rp Acc existence",
	}

	status_code = 200
	return make_response(jsonify(res), status_code)