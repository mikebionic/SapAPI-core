from flask import Blueprint

bp = Blueprint('commerce_admin', __name__)

from main_pack.commerce.admin import routes,ui_category,ui_company