from flask import Blueprint

api = Blueprint('v1_reg_no_api', __name__)

from .routes import *