# -*- coding: utf-8 -*-
from flask import Flask,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from babel import numbers,dates
from datetime import date,datetime,time
from main_pack.config import Config
from flask_babel import Babel,format_date,gettext,lazy_gettext
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
# from elasticsearch import Elasticsearch
babel = Babel()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

# elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])\
# 	if app.config['ELASTICSEARCH_URL'] else None

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
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	login_manager.init_app(app)
	babel.init_app(app)
	mail.init_app(app)
	csrf.init_app(app)
	# elasticsearch.init_app(app)
	
	# all models are separated in the models folder
	from main_pack.models import bp as models_bp
	app.register_blueprint(models_bp)

	from main_pack.main import bp as main_bp
	app.register_blueprint(main_bp)

	from main_pack.base import bp as base_bp
	app.register_blueprint(base_bp)

	# api blueprints
	api_url_prefix = '/ls/api/'
	from main_pack.api.auth import api as auth_api
	app.register_blueprint(auth_api,url_prefix=api_url_prefix)

	from main_pack.api.errors import api as errors_api
	app.register_blueprint(errors_api,url_prefix=api_url_prefix)

	from main_pack.api.commerce import api as commerce_api
	app.register_blueprint(commerce_api,url_prefix=api_url_prefix)

	from main_pack.api.users import api as users_api
	app.register_blueprint(users_api,url_prefix=api_url_prefix)

	csrf.exempt(auth_api)
	csrf.exempt(commerce_api)
	csrf.exempt(users_api)

	# /api blueprints

	# commerce blueprints
	commerce_url_prefix = '/commerce'
	from main_pack.commerce.auth import bp as commerce_auth_bp
	app.register_blueprint(commerce_auth_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.commerce import bp as commerce_bp
	app.register_blueprint(commerce_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.errors import bp as commerce_errors_bp
	app.register_blueprint(commerce_errors_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.users import bp as commerce_users_bp
	app.register_blueprint(commerce_users_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.admin import bp as commerce_admin_bp
	app.register_blueprint(commerce_admin_bp,url_prefix=commerce_url_prefix)
	# /commerce blueprints

	return app
