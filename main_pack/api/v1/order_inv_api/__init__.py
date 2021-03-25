from flask import Blueprint

api = Blueprint('v1_order_inv_api', __name__)

from .routes import *