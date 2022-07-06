from flask import Blueprint

api = Blueprint('v1_rating_api', __name__)

from .routes import *