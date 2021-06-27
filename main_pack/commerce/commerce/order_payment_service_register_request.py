from flask import (
	make_response,
	jsonify,
	request,
	url_for
)

from flask_login import login_required
from main_pack.api.base.validators import request_is_json

from main_pack.commerce.commerce import bp
from main_pack.api.v1.order_inv_api.utils import do_mpi_gov_tm_payment_service_register_request


@bp.route("/order-payment-register-request/", methods=['POST'])
@login_required
@request_is_json(request)
def order_payment_service_register_request():
	online_payment_type = request.args.get("online_payment_type", 1, type=int)
	# online_payment_type = 1 # local state
	# online_payment_type = 2 # interActiv

	req = request.get_json()
	req["OInvRegNo"] = req["RegNo"]

	cart_view_route = url_for('commerce.cart')[1:] if url_for('commerce.cart')[0] == "/" else url_for('commerce.cart')
	return_url = f"{request.url_root}{cart_view_route}"

	if online_payment_type == 1:
		data = do_mpi_gov_tm_payment_service_register_request(req, return_url)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code