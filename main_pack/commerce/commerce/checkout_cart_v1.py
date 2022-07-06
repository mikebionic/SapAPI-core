from flask import (
	request,
	session,
	jsonify,
	abort,
)
from flask_login import current_user
from datetime import datetime

from main_pack.commerce.commerce import bp
from main_pack import gettext

from main_pack.base.apiMethods import get_login_info
from main_pack.api.v1.order_inv_api.utils import save_order_checkout_data
from main_pack.config import Config
from main_pack.models import Rp_acc


@bp.route("/checkout-cart-v1/",methods=['POST'])
def checkout_cart_v1():
	this_rp_acc = None
	if current_user.is_authenticated:
		this_rp_acc = current_user

	elif Config.USE_APP_WITHOUT_AUTH:
		this_rp_acc = Rp_acc.query\
			.filter_by(
				RpAccGuid = Config.WITHOUT_AUTH_CHECKOUT_RPACCGUID,
				GCRecord = None)\
			.first()

		session["model_type"] = "rp_acc"

	if not this_rp_acc:
		abort(401)
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
		res = save_order_checkout_data(req, session["model_type"], this_rp_acc, session)

		if res["status"] == 1:
			response["responseText"] = gettext('Checkout')+' '+gettext('successfully done')+'! '+gettext('View orders in profile page.')
			response["status"] = 1
			response["data"] = res["data"]

		else:
			raise Exception

	except Exception as ex:
		print(f"{datetime.now()} | UI_checkout Exception: {ex}")

	return jsonify(response)