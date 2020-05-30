from flask import Blueprint

api = Blueprint('users_api', __name__)

from main_pack.api.users import users_api