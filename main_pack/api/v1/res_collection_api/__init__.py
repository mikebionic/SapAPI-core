from flask import Blueprint

api = Blueprint('v1_res_collection_api', __name__)

from .routes import *