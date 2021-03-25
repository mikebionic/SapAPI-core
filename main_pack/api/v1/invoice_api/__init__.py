from flask import Blueprint

api = Blueprint('v1_invoice_api', __name__)

from .routes import *