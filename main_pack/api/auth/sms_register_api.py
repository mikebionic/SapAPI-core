
from flask import request

from main_pack import lazy_gettext
from main_pack.api.auth import api
from main_pack.api.auth.register_phone_number import (
	login_phone_number,
	register_phone_number,
	check_phone_number_register,
	verify_phone_number_register,
)
from main_pack.api.auth.utils import sha_required
from main_pack.api.response_handlers import handle_default_response

from main_pack.base import log_print
from main_pack.config import Config


@api.route('/verify-sms-register/',methods=['POST'])
@sha_required
def verify_sms_register():
	req = request.get_json()
	phone_number = req.get('phone_number')
	message_text = req.get('message_text')

	verify_phone_number_register(phone_number, message_text)

	return handle_default_response(req)


@api.route("/request-sms-register/")
def request_sms_register():
	data, message = {}, ""

	try:
		header_data = request.headers
		if "PhoneNumber" not in header_data:
			raise Exception

		data, message = register_phone_number(header_data["PhoneNumber"])

	except Exception as ex:
		log_print(f"SMS register exception: {ex}", "warning")

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

	return handle_default_response(data, message, status_code=200)


# !!! Todo change to single route with args
@api.route("/request-sms-login/")
def request_sms_login():
	data, message = {}, ""

	try:
		header_data = request.headers
		if "PhoneNumber" not in header_data:
			raise Exception

		data, message = login_phone_number(header_data["PhoneNumber"])

	except Exception as ex:
		log_print(f"SMS login exception: {ex}", "warning")

	message = "{}: <h4>{}</h4>\n {} {} {}".format(
		lazy_gettext('Send an empty SMS to number'),
		f'''<div style="margin: 1rem 0">
		<a href="sms:{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}">
		{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}</a>
		<a class="btn btn-success" style="margin-left: 1rem" href="sms:{Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER}">
		Send</a>
		</div>
		''',
		lazy_gettext('Request expires in'),
		Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES,
		"(minutes)") if data else message or "Login request"

	return handle_default_response(data, message, status_code=200)


@api.route("/check-sms-register/")
def check_sms_register():

	data, message = {}, ""
	response_headers = {}

	try:
		header_data = request.headers
		if "PhoneNumber" not in header_data:
			raise Exception

		data, message = check_phone_number_register(header_data["PhoneNumber"])
		if data:
			if "token" in data:
				response_headers["token"] = data["token"]

	except Exception as ex:
		log_print(f"SMS register check exception: {ex}", "warning")

	message = "{}"\
		.format("Register check success") if data else message or "Register request check"

	return handle_default_response(data, message, headers = response_headers, status_code=200)