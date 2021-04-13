from flask import (
	make_response,
	jsonify
)

from main_pack.config import Config
from main_pack.api.v1.payment_info_api import api


@api.route('/payment-validation-service-info/')
def payment_validation_service_info():
	data = {}
	if Config.ALLOW_PAYMENT_INFO_API:
		data = {
			"PAYMENT_VALIDATION_SERVICE_URL": Config.PAYMENT_VALIDATION_SERVICE_URL,
			"PAYMENT_VALIDATION_SERVICE_USERNAME": Config.PAYMENT_VALIDATION_SERVICE_USERNAME,
			"PAYMENT_VALIDATION_SERVICE_PASSWORD": Config.PAYMENT_VALIDATION_SERVICE_PASSWORD,
		}
	return make_response(jsonify(data)), 200