# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import validate_order_inv_payment


@api.route("/order-inv-validation/", methods=['POST'])
@token_required
@request_is_json(request)
def order_inv_validation_post(user):
	current_user = user['current_user']
	model_type = user['model_type']
	req = request.get_json()

	data, status, message = validate_order_inv_payment(req, model_type, current_user)

	res = {
		"data": data,
		"message": message,
		"status": status,
		"total": len(data)
	}

	status_code = 200 if res["status"] == 0 else 201
	response = make_response(jsonify(res), status_code)

	return response