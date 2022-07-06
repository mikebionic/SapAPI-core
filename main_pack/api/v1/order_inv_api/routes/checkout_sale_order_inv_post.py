# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify, session

from main_pack.api.auth.utils import checkout_auth_handler
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import get_login_info

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import save_order_checkout_data
from main_pack import csrf

@csrf.exempt
@api.route("/checkout-sale-order-inv/", methods=['POST'])
@checkout_auth_handler
@request_is_json(request)
def checkout_sale_order_inv_post(user):
	model_type = user['model_type']
	current_user = user['current_user']
	req = request.get_json()

	request_info = get_login_info(request)
	device_info_from_req = req.copy()
	device_info_from_req['orderInv'] = {}
	req['orderInv']['AddInf5'] = f"{str(device_info_from_req)} | {str(request_info)}"

	res = save_order_checkout_data(req, model_type, current_user, session)

	status_code = 400 if res["status"] != 1 else 201
	return make_response(jsonify(res), status_code)