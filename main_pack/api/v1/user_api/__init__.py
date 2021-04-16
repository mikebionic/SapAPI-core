from flask import Blueprint

api = Blueprint('v1_user_api', __name__)

from .routes import *