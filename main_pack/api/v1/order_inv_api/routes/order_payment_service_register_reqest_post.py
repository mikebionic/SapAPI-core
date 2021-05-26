from flask import (
	make_response,
	jsonify,
	request,
)

from main_pack.api.v1.order_inv_api import api
from main_pack.api.v1.order_inv_api.utils import do_mpi_gov_tm_payment_service_register_request

@api.route("/order-payment-register-request/", methods=['POST'])
def order_payment_service_register_request_post():
	req = request.get_json()
	data = do_mpi_gov_tm_payment_service_register_request(req)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code
