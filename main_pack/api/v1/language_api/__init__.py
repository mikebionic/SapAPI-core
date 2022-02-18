from flask import Blueprint

api = Blueprint('v1_language_api', __name__)

from .routes import *