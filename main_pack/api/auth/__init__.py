from flask import Blueprint

api = Blueprint('auth_api', __name__)

from main_pack.api.auth import (
	api_login,
	api_register,
	sms_register_api,
	attempt_counter,
	email_auth_utils,
	register_api,
	register_phone_number,
)