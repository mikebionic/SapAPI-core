from flask import Blueprint

api = Blueprint('auth_api_test', __name__)

from main_pack.api_test.auth import api_login
