from flask import Blueprint

api = Blueprint('activation_customer_api',__name__)

from . import (
	device_register,
	device_fetch
)