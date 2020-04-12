from flask import Blueprint

bp = Blueprint('admin', __name__)

from main_pack.commerce.admin import routes
