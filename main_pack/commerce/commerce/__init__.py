from flask import Blueprint

bp = Blueprint('commerce',__name__)

from main_pack.commerce.commerce import (
	routes,
	ui_cart,
	v_products,
	ui_wishlist,
	ui_rating)