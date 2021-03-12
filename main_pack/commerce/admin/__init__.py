from flask import Blueprint

from main_pack.config import Config

bp = Blueprint('commerce_admin',__name__)
url_prefix = Config.COMMERCE_ADMIN_URL_PREFIX

from . import (
	admin_auth,
	routes,
	ui_category,
	ui_company,
	ui_resource,
	ui_barcode,
	ui_price,
	ui_translations,
	ui_images,
	ui_properties,
	images_setup,
	ui_sliders,
	ui_invoices,
	ui_users_customers,
	ui_rating
)