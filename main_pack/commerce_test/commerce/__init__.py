from flask import Blueprint

bp = Blueprint('commerce_test',__name__)

from main_pack.commerce_test.commerce import (routes,
                                        ui_cart,
                                        v_products,
                                        ui_wishlist,
                                        ui_rating)