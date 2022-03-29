
from flask import request

from main_pack import lazy_gettext
from main_pack.base import log_print
from main_pack.config import Config
from main_pack.api.response_handlers import handle_default_response

from main_pack.api.auth import api
from main_pack.api.auth.register_phone_number import (
	register_phone_number,
)
from main_pack.api.auth.auth_utils import register_email, verify_email_register, verify_phone_number_register


@api.route("/register-request/")
def register_request():
	data, message = {}, ""

	register_method = request.args.get("method","email",type=str)
	header_data = request.headers

	try:
		if register_method == "email":
			if "Email" not in header_data:
				log_print(f"Email not in header {str(header_data)}")
				raise Exception

			data, message = register_email(header_data["Email"])
			message = "{}, {}\n {} {} {}".format(
				header_data["Email"],
				lazy_gettext('An email has been sent with instructions to register your profile'),
				lazy_gettext('Request expires in'),
				Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES,
				"(minutes)") if data else message or "Register request"

		if register_method == "phone_number":
			if "PhoneNumber" not in header_data:
				log_print(f"PhoneNumber not in header {str(header_data)}")
				raise Exception

			data, message = register_phone_number(header_data["PhoneNumber"])
			message = "{}: <h4>{}</h4>\n {} {} {}".format(
				lazy_gettext('Send an empty SMS to number'),
				f'''<div style="margin: 1rem 0">
				<a href="sms:{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}">
				{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}</a>
				<a class="btn btn-success" style="margin-left: 1rem" href="sms:{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}">
				{lazy_gettext('Send')}</a>
				</div>
				''',
				lazy_gettext('Request expires in'),
				Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES,
				"(minutes)") if data else message or "Register request"

	except Exception as ex:
		log_print(f"Register request exception: {ex}", "warning")

	return handle_default_response(data, message, status_code=200)


@api.route('/verify-register/',methods=['POST'])
def verify_register():
	data, message = {}, "Register verify api"
	response_headers = {}
	register_method = request.args.get("method","email",type=str)

	try:
		req = request.get_json()
		if register_method == "email":
			email = req.get('email')
			verify_code = req.get('verify_code')
			data, message = verify_email_register(email, verify_code)

		if register_method == "phone_number":
			phone_number = req.get('phone_number')
			verify_code = req.get('verify_code')
			data, message = verify_phone_number_register(phone_number, verify_code)

		if data:
			if "token" in data:
				response_headers["token"] = data["token"]

	except Exception as ex:
		log_print(f"Verify register route exception: {ex}", "warning")

	return handle_default_response(data, message, headers = response_headers, status_code=200)
