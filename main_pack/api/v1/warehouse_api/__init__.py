from flask import Blueprint

api = Blueprint('v1_warehouse_api', __name__)

from .routes import *