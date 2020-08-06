import sys
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
	SECRET_KEY = environ.get('SECRET_KEY')
	SYNCH_SHA = environ.get('SYNCH_SHA')

	# set to production if Production
	FLASK_ENV = 'development'
	# set to false to turn off debugging
	DEBUG = True
	TESTING = True

	# SQLALCHEMY_DATABASE_URI = 'sqlite:///commerce.db'

	POSTGRES_DB_URI = {
	    'user': environ.get('POSTGRES_DB_USERNAME'),
	    'pw': environ.get('POSTGRES_DB_PASSWORD'),
	    'db': environ.get('POSTGRES_DB_DATABASE'),
	    'host': environ.get('POSTGRES_DB_HOST'),
	    'port': environ.get('POSTGRES_DB_PORT'),
	}
	SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_DB_URI

	# default language for session
	BABEL_DEFAULT_LOCALE = 'tk'

	# MAIL CONFIGURATION
	MAIL_SERVER = environ.get('MAIL_SERVER')
	MAIL_PORT = environ.get('MAIL_PORT')
	MAIL_USE_TLS = environ.get('MAIL_USE_TLS')
	MAIL_USERNAME = environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

	# set to True if you want to use BCrypt hashing
	HASHED_PASSWORDS = False

	# # to give each api it's pagination: 
	RESOURCES_PER_PAGE = 15
	API_OBJECTS_PER_PAGE = 10

	# REG_NO generator's random range
	REG_NUM_RANDOM_RANGE = 10000

	# # elasticsearch search engine's url
	# ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')

	# get OS Type to configure app for Windows or Linux
	OS_TYPE = sys.platform

	# set to True if you want to sell resources
	# if no left in Res_total.ResPendingTotalAmount
	NEGATIVE_WH_QTY_SALE = False
	NEGATIVE_WH_QTY_ORDER = True

	# # ability to make an order if qty of resoruce
	# # is greater than Res_total in warehouse
	# OVERRIDE_WH_QTY_ORDER = True

	# set to True to show resources
	# if no left in Res_total.ResTotBalace
	SHOW_NEGATIVE_WH_QTY_RESOURCE = True

	# language and currency of price-to-text converter
	PRICE_2_TEXT_LANGUAGE = 'tk'
	# PRICE_2_TEXT_LANGUAGE = 'en'
	# PRICE_2_TEXT_LANGUAGE = 'ru'
	PRICE_2_TEXT_CURRENCY = 'TMT'
	# PRICE_2_TEXT_CURRENCY = 'USD'
	# PRICE_2_TEXT_CURRENCY = 'RUB'

	# icon extentions and size
	ALLOWED_ICON_EXTENSIONS = set(['png','jpg','jpeg','svg'])
	ALLOWED_IMAGE_EXTENSIONS = set(['png','jpg','jpeg'])
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
