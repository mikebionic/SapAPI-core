from flask import (
	request,
	session,
	jsonify,
)
from flask_login import login_required, current_user
from datetime import datetime

from main_pack.commerce.commerce import bp
from main_pack import gettext

from main_pack.base.apiMethods import get_login_info
from main_pack.api.v1.order_inv_api.utils import save_order_checkout_data


@bp.route("/checkout-cart-v1/",methods=['POST'])
@login_required
def checkout_cart_v1():
	req = request.get_json()

	response = {
		"status": 0,
		"responseText": gettext('Unknown error!'),
		"data": {},
	}

	try:
		if session["model_type"] == "user":
			raise Exception

		if not req['orderInv']:
			raise Exception

		if not req['orderInv']['PmId']:
			response["responseText"] = gettext('Specify the payment method')
			return jsonify(response)

		req['orderInv']['AddInf5'] = str(get_login_info(request))
		res = save_order_checkout_data(req, session["model_type"], current_user, session)

		if res["status"] == 1:
			response["responseText"] = gettext('Checkout')+' '+gettext('successfully done')+'! '+gettext('View orders in profile page.')
			response["status"] = 1
			response["data"] = res["data"]

		else:
			raise Exception

	except Exception as ex:
		print(f"{datetime.now()} | UI_checkout Exception: {ex}")

	return jsonify(response)