from flask import Blueprint

api = Blueprint('v1_translation_api', __name__)

from .routes import *