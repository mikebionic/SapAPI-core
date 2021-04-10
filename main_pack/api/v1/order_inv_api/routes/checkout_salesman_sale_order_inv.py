# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.api.v1.checkout_salesman_order_inv_api import api
from main_pack.api.v1.checkout_salesman_order_inv_api.utils import save_order_checkout_data


@api.route("/checkout-salesman-sale-order-inv/", methods=['POST'])
@token_required
@request_is_json(request)
def checkout_salesman_sale_order_inv(user):
	model_type = user['model_type']
	current_user = user['current_user']
	req = request.get_json()
	data, fails = save_order_checkout_data(req, model_type, current_user)
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