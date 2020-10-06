from flask import Blueprint

api = Blueprint('commerce_api',__name__)

from main_pack.api.errors import routes
from main_pack.api.commerce import (category_api,
																		barcode_api,
																		image_api,
																		res_price_api,
																		res_total_api,
																		rp_acc_api,
																		rp_acc_total_api,
																		order_inv_api,
																		invoice_api,
																		order_inv_line_api,
																		order_inv_type_api,
																		checkout_order_inv_api,
																		resource_api,
																		resource_v_api,
																		slider_api,
																		warehouse_api,
																		users_api,
																		work_period_api,
																		config_info_api,
																		payment_api)