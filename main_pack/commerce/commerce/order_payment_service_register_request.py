from flask import (
	make_response,
	jsonify,
	request,
	url_for
)

from flask_login import login_required
from main_pack.api.base.validators import request_is_json

from main_pack.commerce.commerce import bp
from main_pack.api.v1.order_inv_api.utils import do_halkbank_payment_service_register_request


@bp.route("/order-payment-register-request/", methods=['POST'])
@login_required
@request_is_json(request)
def order_payment_service_register_request():
	online_payment_type = request.args.get("online_payment_type", "halkbank", type=str).strip()

	# online_payment_type = "halkbank" # local state
	# online_payment_type = "foreign_affairs_bank" # interActiv

	req = request.get_json()
	req["OInvRegNo"] = req["RegNo"]

	paym_validation_view = url_for('commerce.render_payment_validation_view')[1:] if url_for('commerce.render_payment_validation_view')[0] == "/" else url_for('commerce.render_payment_validation_view')
	return_url = f"{request.url_root}{paym_validation_view}"

	data = {}
	if online_payment_type == "halkbank":
		data = do_halkbank_payment_service_register_request(req, return_url)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code