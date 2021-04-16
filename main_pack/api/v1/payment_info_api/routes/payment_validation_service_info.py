from flask import (
	make_response,
	jsonify
)

from main_pack.api.common import get_payment_validation_info
from main_pack.api.v1.payment_info_api import api


@api.route('/payment-validation-service-info/')
def payment_validation_service_info():
	data = get_payment_validation_info()
	return make_response(jsonify(data)), 200