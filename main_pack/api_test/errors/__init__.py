from flask import Blueprint

api = Blueprint('api_errors_test', __name__)

from main_pack.api_test.errors import routes