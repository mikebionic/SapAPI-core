from flask import Blueprint

bp = Blueprint('auth', __name__)

from main_pack.commerce.auth import routes
