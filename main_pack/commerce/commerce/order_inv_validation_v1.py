# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify, session
from datetime import datetime
from flask_login import login_required, current_user
from main_pack.api.base.validators import request_is_json

from main_pack.commerce.commerce import bp
from main_pack import gettext
from main_pack.api.v1.order_inv_api.utils import validate_order_inv_payment


@bp.route("/order-inv-validation/", methods=['POST'])
@login_required
@request_is_json(request)
def order_inv_validation_v1():
	req = request.get_json()
	response = {
		"status": 0,
		"responseText": gettext('Unknown error!'),
		"data": {},
	}

	try:
		if session["model_type"] == "user":
			raise Exception

		data, status, message = validate_order_inv_payment(req, session["model_type"], current_user)

		response["status"] = status
		response["responseText"] = gettext('Checkout')+' '+gettext('successfully done')+'! '+gettext('View orders in profile page.')
		response["data"] = data
		if status != 1:
			response["responseText"] = message if message else gettext('Unknown error!')

	except Exception as ex:
		print(f"{datetime.now()} | UI_payment_validation Exception: {ex}")

	return make_response(jsonify(response))