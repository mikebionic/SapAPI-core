from flask import Blueprint

bp = Blueprint('commerce_auth', __name__)

from main_pack.commerce.auth import routes
