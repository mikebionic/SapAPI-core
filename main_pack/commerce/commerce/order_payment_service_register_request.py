from flask import (
	make_response,
	jsonify,
	request,
)

from flask_login import login_required
from main_pack.api.base.validators import request_is_json

from main_pack.commerce.commerce import bp
from main_pack.api.v1.order_inv_api.utils import do_mpi_gov_tm_payment_service_register_request

@bp.route("/order-payment-register-request/", methods=['POST'])
@login_required
@request_is_json(request)
def order_payment_service_register_request():
	req = request.get_json()
	data = do_mpi_gov_tm_payment_service_register_request(req)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code