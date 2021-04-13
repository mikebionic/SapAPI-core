from flask import Blueprint

api = Blueprint('v1_payment_info_api', __name__)

from .routes import *