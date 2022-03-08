from flask import Blueprint

api = Blueprint('v1_resource_api', __name__)

from .routes import *