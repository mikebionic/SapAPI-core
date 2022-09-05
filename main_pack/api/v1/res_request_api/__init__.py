from flask import Blueprint

api = Blueprint('v1_res_request_api', __name__)

from .routes import *