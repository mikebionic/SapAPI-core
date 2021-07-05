# -*- coding: utf-8 -*-
from flask import Flask,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from babel import numbers,dates
from datetime import datetime
from flask_babel import Babel,format_date,gettext,lazy_gettext
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
import logging
from logging.handlers import SMTPHandler
from htmlmin.main import minify

from main_pack.config import Config

babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()
cache = Cache()
compress = Compress()


login_manager.login_view = 'commerce_auth.login'
login_manager.login_message = lazy_gettext('Login the system!')
login_manager.login_message_category = 'info'

@babel.localeselector
def get_locale():
	try:
		language = session['language']
	except KeyError:
		# language = None
		session['language'] = 'tk'
		language = session['language']
	if language is not None:
		return language
	return 'tk'

LANGUAGES = {
	'en': 'English',
	'tk': 'Turkmen',
	'ru': 'Russian'
}

def create_app(config_class=Config):
	app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH)
	app.config.from_object(Config)
	app.static_folder = Config.STATIC_FOLDER_LOCATION
	app.template_folder = Config.TEMPLATE_FOLDER_LOCATION
	if Config.USE_FLASK_CORS:
		CORS(app)

	db.init_app(app)
	login_manager.init_app(app)
	babel.init_app(app)
	mail.init_app(app)
	csrf.init_app(app)
	cache.init_app(app)

	if Config.USE_FLASK_COMPRESS:
		compress.init_app(app)

	if Config.OS_TYPE != 'win32':
		sess.init_app(app)

	from main_pack.main import bp as main_bp
	app.register_blueprint(main_bp)

	from main_pack.base import bp as base_bp
	app.register_blueprint(base_bp)

	from main_pack.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	# api blueprints
	api_url_prefix = Config.API_URL_PREFIX

	from main_pack.api.auth import api as auth_api
	app.register_blueprint(auth_api, url_prefix=api_url_prefix)

	from main_pack.api.base import api as base_api
	app.register_blueprint(base_api, url_prefix=api_url_prefix)

	from main_pack.api.commerce import api as commerce_api
	app.register_blueprint(commerce_api, url_prefix=api_url_prefix)

	from main_pack.api.users import api as users_api
	app.register_blueprint(users_api, url_prefix=api_url_prefix)


	from main_pack.api.v1.rp_acc_api import api as v1_rp_acc_api
	app.register_blueprint(v1_rp_acc_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_rp_acc_api)

	from main_pack.api.v1.user_api import api as v1_user_api
	app.register_blueprint(v1_user_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_user_api)

	from main_pack.api.v1.invoice_api import api as v1_invoice_api
	app.register_blueprint(v1_invoice_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_invoice_api)

	from main_pack.api.v1.order_inv_api import api as v1_order_inv_api
	app.register_blueprint(v1_order_inv_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_order_inv_api)

	from main_pack.api.v1.warehouse_api import api as v1_warehouse_api
	app.register_blueprint(v1_warehouse_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_warehouse_api)

	from main_pack.api.v1.payment_info_api import api as v1_payment_info_api
	app.register_blueprint(v1_payment_info_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_payment_info_api)

	from main_pack.api.v1.session_api import api as v1_session_api
	app.register_blueprint(v1_session_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_session_api)

	from main_pack.api.v1.image_api import api as v1_image_api
	app.register_blueprint(v1_image_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_image_api)

	from main_pack.api.v1.media_api import api as v1_media_api
	app.register_blueprint(v1_media_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_media_api)

	from main_pack.api.v1.device_api import api as v1_device_api
	app.register_blueprint(v1_device_api, url_prefix=f"{api_url_prefix}/v1/")
	csrf.exempt(v1_device_api)

	if Config.USE_ACTIVATION_CUSTOMER:
		from main_pack.activation.customer import api as activation_customer_api
		app.register_blueprint(activation_customer_api, url_prefix=api_url_prefix)
		csrf.exempt(activation_customer_api)

	if Config.USE_ACTIVATION_SERVER:
		sap_service_url_prefix = Config.SAP_SERVICE_URL_PREFIX
		from main_pack.activation.server import api as activation_server_api
		app.register_blueprint(activation_server_api, url_prefix=sap_service_url_prefix)
		csrf.exempt(activation_server_api)

	csrf.exempt(auth_api)
	csrf.exempt(base_api)
	csrf.exempt(commerce_api)
	csrf.exempt(users_api)
	# /api blueprints

	# commerce blueprints
	commerce_url_prefix = Config.COMMERCE_URL_PREFIX

	from main_pack.commerce.admin import bp as commerce_admin_bp
	app.register_blueprint(commerce_admin_bp, url_prefix=Config.COMMERCE_ADMIN_URL_PREFIX)

	if not Config.API_AND_ADMIN_ONLY:

		from main_pack.commerce.auth import bp as commerce_auth_bp
		app.register_blueprint(commerce_auth_bp, url_prefix=commerce_url_prefix)

		from main_pack.commerce.commerce import bp as commerce_bp
		app.register_blueprint(commerce_bp, url_prefix=commerce_url_prefix)

		from main_pack.commerce.users import bp as commerce_users_bp
		app.register_blueprint(commerce_users_bp, url_prefix=commerce_url_prefix)

	else:
		login_manager.login_view = 'commerce_admin.login'
	# /commerce blueprints

	# logging
	if not Config.DEBUG:
		if (Config.EMAIL_ERROR_REPORTS and Config.MAIL_SERVER):
			auth = None
			if (Config.MAIL_USERNAME and Config.MAIL_PASSWORD):
				auth = (Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
			secure = None
			if Config.MAIL_USE_TLS:
				secure = ()
			mail_handler = SMTPHandler(
				mailhost = (Config.MAIL_SERVER, Config.MAIL_PORT),
				fromaddr = 'no-reply@' + Config.MAIL_SERVER,
				toaddrs = Config.EMAIL_ERROR_REPORTS_ADDRESSES, subject = f'[{Config.COMPANY_NAME}] App Error occured at {datetime.now()}',
				credentials = auth,
				secure = secure)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)
	# /logging

	if Config.MINIFY_HTML_RESPONSE:
		@app.after_request
		def response_minify(response):
			if response.content_type == u'text/html; charset=utf-8':
				response.set_data(minify(response.get_data(as_text=True)))
				return response
			return response

	return app