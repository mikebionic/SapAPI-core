from flask import Blueprint

api = Blueprint('auth_api', __name__)

from main_pack.api.auth import (
	api_login,
	sms_register_api,
	attempt_counter,
)