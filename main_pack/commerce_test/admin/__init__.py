from flask import Blueprint

bp = Blueprint('commerce_admin_test',__name__)

from main_pack.commerce_test.admin import routes,ui_category,ui_company,ui_resource
from main_pack.commerce_test.admin import (ui_barcode,
																			ui_price,
																			ui_translations,
																			ui_images,
																			ui_properties,
																			images_setup,
																			ui_sliders,
																			ui_invoices,
																			ui_users_customers)