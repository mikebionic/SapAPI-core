from flask import Blueprint

api = Blueprint('v1_status_api', __name__)

from .routes import *