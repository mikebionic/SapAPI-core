from flask import Blueprint

api = Blueprint('api_errors', __name__)

from main_pack.api.errors import routes