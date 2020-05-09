from flask import Blueprint

bp = Blueprint('commerce_admin', __name__)

from main_pack.commerce.admin import routes,ui_category,ui_company,ui_resource
from main_pack.commerce.admin import (ui_barcode,ui_price,ui_translations,ui_images)