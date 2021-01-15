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
import logging
from logging.handlers import SMTPHandler

from main_pack.config import Config


babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()

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
	app = Flask(__name__, static_url_path='/ls/static')
	app.config.from_object(Config)

	if Config.USE_FLASK_CORS:
		CORS(app)

	db.init_app(app)
	login_manager.init_app(app)
	babel.init_app(app)
	mail.init_app(app)
	csrf.init_app(app)
	if Config.OS_TYPE != 'win32':
		sess.init_app(app)

	# all models are separated in the models folder
	from main_pack.models import bp as models_bp
	app.register_blueprint(models_bp)

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

	if Config.USE_ACTIVATION_SERVICE:
		from main_pack.activation.customer import api as activation_customer_api
		app.register_blueprint(activation_customer_api, url_prefix=api_url_prefix)
		csrf.exempt(activation_customer_api)

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
	app.register_blueprint(commerce_admin_bp, url_prefix=commerce_url_prefix)

	from main_pack.commerce.auth import bp as commerce_auth_bp
	app.register_blueprint(commerce_auth_bp, url_prefix=commerce_url_prefix)

	if not Config.API_AND_ADMIN_ONLY:

		from main_pack.commerce.commerce import bp as commerce_bp
		app.register_blueprint(commerce_bp, url_prefix=commerce_url_prefix)

		from main_pack.commerce.users import bp as commerce_users_bp
		app.register_blueprint(commerce_users_bp, url_prefix=commerce_url_prefix)

	else:
		login_manager.login_view = 'commerce_auth.admin_login'
	# /commerce blueprints

	# logging
	if not Config.DEBUG:
		if (Config.EMAIL_ERROR_REPORTS and Config.MAIL_SERVER):
			auth = None
			if Config.MAIL_ADDRESS or Config.MAIL_PASSWORD:
				auth = (Config.MAIL_ADDRESS, Config.MAIL_PASSWORD)
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

	return app