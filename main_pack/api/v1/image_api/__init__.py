from flask import Blueprint

api = Blueprint('v1_image_api', __name__)

from .routes import *