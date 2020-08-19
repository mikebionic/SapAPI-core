from flask import Blueprint
from main_pack.config import Config

bp = Blueprint('commerce_admin',__name__)
url_prefix = Config.COMMERCE_URL_PREFIX

from main_pack.commerce.admin import routes,ui_category,ui_company,ui_resource
from main_pack.commerce.admin import (ui_barcode,
																			ui_price,
																			ui_translations,
																			ui_images,
																			ui_properties,
																			images_setup,
																			ui_sliders,
																			ui_invoices,
																			ui_users_customers)