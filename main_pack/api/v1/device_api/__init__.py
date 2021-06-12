from flask import Blueprint

api = Blueprint('v1_device_api', __name__)

from .routes import *