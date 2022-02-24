from flask import Blueprint

api = Blueprint('v1_api', __name__)

from main_pack.api.v1.rp_acc_api import api as v1_rp_acc_api
api.register_blueprint(v1_rp_acc_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_rp_acc_api)

from main_pack.api.v1.user_api import api as v1_user_api
api.register_blueprint(v1_user_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_user_api)

from main_pack.api.v1.invoice_api import api as v1_invoice_api
api.register_blueprint(v1_invoice_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_invoice_api)

from main_pack.api.v1.order_inv_api import api as v1_order_inv_api
api.register_blueprint(v1_order_inv_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_order_inv_api)

from main_pack.api.v1.warehouse_api import api as v1_warehouse_api
api.register_blueprint(v1_warehouse_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_warehouse_api)

from main_pack.api.v1.payment_info_api import api as v1_payment_info_api
api.register_blueprint(v1_payment_info_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_payment_info_api)

from main_pack.api.v1.session_api import api as v1_session_api
api.register_blueprint(v1_session_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_session_api)

from main_pack.api.v1.image_api import api as v1_image_api
api.register_blueprint(v1_image_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_image_api)

from main_pack.api.v1.media_api import api as v1_media_api
api.register_blueprint(v1_media_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_media_api)

from main_pack.api.v1.barcode_api import api as v1_barcode_api
api.register_blueprint(v1_barcode_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_barcode_api)

from main_pack.api.v1.device_api import api as v1_device_api
api.register_blueprint(v1_device_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_device_api)

from main_pack.api.v1.translation_api import api as v1_translation_api
api.register_blueprint(v1_translation_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_translation_api)

from main_pack.api.v1.language_api import api as v1_language_api
api.register_blueprint(v1_language_api) #, url_prefix=f"{api_url_prefix}/v1/")
# csrf.exempt(v1_language_api)