from flask import Blueprint

from main_pack.config import Config

bp = Blueprint('commerce',__name__)
url_prefix = Config.COMMERCE_URL_PREFIX

from main_pack.commerce.commerce import (
	routes,
	ui_cart,
	v_products,
	ui_wishlist,
	ui_rating,
	checkout_cart_v1,
)