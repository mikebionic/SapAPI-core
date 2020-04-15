from flask import Flask,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from babel import numbers,dates
from datetime import date,datetime,time
from main_pack.config import Config
from flask_babel import Babel,format_date,gettext,lazy_gettext
from flask_bcrypt import Bcrypt
from flask_mail import Mail

babel = Babel()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login_commerce'
login_manager.login_message = lazy_gettext('Login the system!')
login_manager.login_message_category = 'info'

@babel.localeselector
def get_locale():
	try:
		language = session['language']
	except KeyError:
		language = None
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
	
	# all models are separated in the models folder
	from main_pack.models import bp as models_bp
	app.register_blueprint(models_bp)

	# commerce blueprints
	commerce_url_prefix = '/commerce'
	from main_pack.commerce.auth import bp as commerce_auth_bp
	app.register_blueprint(commerce_auth_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.commerce import bp as commerce_bp
	app.register_blueprint(commerce_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.errors import bp as commerce_errors_bp
	app.register_blueprint(commerce_errors_bp,url_prefix=commerce_url_prefix)

	# from main_pack.commerce.users import bp as commerce_users_bp
	# app.register_blueprint(commerce_users_bp,url_prefix=commerce_url_prefix)

	from main_pack.commerce.admin import bp as commerce_admin_bp
	app.register_blueprint(commerce_admin_bp,url_prefix=commerce_url_prefix)
	# /commerce blueprints

	return app