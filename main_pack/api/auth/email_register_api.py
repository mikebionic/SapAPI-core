
from flask import request

from main_pack import lazy_gettext
from main_pack.base import log_print
from main_pack.config import Config
from main_pack.api.response_handlers import handle_default_response

from main_pack.api.auth import api
from main_pack.api.auth.register_phone_number import (
	register_phone_number,
	check_phone_number_register,
)
from main_pack.api.auth.email_auth_utils import register_email


@api.route("/register-request/")
def register_request():
	data = {}
	message = ""

	register_method = request.args.get("method","email",type=str)
	header_data = request.headers

	try:
		if register_method == "email":
			if "email" not in header_data:
				raise Exception
			
			data, message = register_email(header_data["email"])
			message = "{}, {}\n {} {} {}".format(
				header_data["email"],
				lazy_gettext('An email has been sent with instructions to register your profile'),
				lazy_gettext('Request expires in'),
				Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES,
				"(minutes)") if data else message or "Register request"

		if register_method == "phone_number":
			if "phone_number" not in header_data:
				raise Exception

			data, message = register_phone_number(header_data["phone_number"])
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


@api.route("/check-register/")
def check_register():

	data = {}
	response_headers = {}

	try:
		header_data = request.headers
		if "phone_number" not in header_data:
			raise Exception

		data, message = check_phone_number_register(header_data["phone_number"])
		if data:
			if "token" in data:
				response_headers["token"] = data["token"]

	except Exception as ex:
		log_print(f"register check exception: {ex}", "warning")

	message = "{}"\
		.format("Register check success") if data else message or "Register request check"

	return handle_default_response(data, message, headers = response_headers, status_code=200)