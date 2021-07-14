from flask import Blueprint

api = Blueprint('v1_barcode_api', __name__)

from .routes import *