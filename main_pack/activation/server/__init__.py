from flask import Blueprint

api = Blueprint('activation_server_api',__name__)

from . import (
	phone_register
)