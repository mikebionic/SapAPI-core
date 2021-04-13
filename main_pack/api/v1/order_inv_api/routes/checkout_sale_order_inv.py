# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify, session

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import save_order_checkout_data


@api.route("/checkout-sale-order-inv/", methods=['POST'])
@token_required
@request_is_json(request)
def checkout_sale_order_inv(user):
	model_type = user['model_type']
	current_user = user['current_user']
	req = request.get_json()

	res = save_order_checkout_data(req, model_type, current_user, session)

	status_code = 400 if res["status"] != 1 else 201
	return make_response(jsonify(res), status_code)