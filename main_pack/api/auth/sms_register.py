
from flask import (
	jsonify,
	request,
	make_response,
)

from main_pack.api.auth import api
from main_pack.api.auth.register_phone_number import register_phone_number

from main_pack.base import log_print

@api.route('/verify-sms-register/',methods=['POST'])
def verify_sms_register():
	req = request.get_json()
	print("headers: ", request.headers)
	print("phone: ", req.get('phone_number'))
	print("message: ", req.get('message_text'))
	return make_response(jsonify(req))


@api.route("/request-sms-register/")
def request_sms_register():
	header_data = request.headers
	try:
		if "PhoneNumber" not in header_data:
			raise Exception

		data = register_phone_number(header_data["PhoneNumber"])
	
	except Exception as ex:
		log_print(f"UI SMS register exception: {ex}", "warning")
	
	res = {
		"data": data,
		"status": 1 if data else 0,
		"total": 1 if data else 0,
		"message": "Register request"
	}
	status_code = 201 if data else 200
	return make_response(jsonify(res)), status_code
