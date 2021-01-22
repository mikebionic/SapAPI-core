import sys
import redis
import json
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
	# get OS Type to configure app for Windows or Linux
	OS_TYPE = sys.platform

	# basic app configs (required)
	SECRET_KEY = environ.get('SECRET_KEY')
	SYNCH_SHA = environ.get('SYNCH_SHA')
	C_MAIN_DIVGUID = environ.get('C_MAIN_DIVGUID')
	MAIN_CGUID = environ.get('MAIN_CGUID')

	SAP_SERVICE_KEY = environ.get('SAP_SERVICE_KEY')
	SAP_SERVICE_URL = environ.get('SAP_SERVICE_URL')
	SAP_SERVICE_URL_PREFIX = environ.get('SAP_SERVICE_URL_PREFIX')
	USE_ACTIVATION_SERVICE = int(environ.get('USE_ACTIVATION_SERVICE'))

	# set to production if Production
	FLASK_ENV = 'development'

	# set to false to turn off debugging
	DEBUG = (int(environ.get('DEBUG')))
	TESTING = (int(environ.get('TESTING')))

	USE_FLASK_CORS = int(environ.get('USE_FLASK_CORS'))
	USE_FLASK_CACHE = int(environ.get('USE_FLASK_CACHE'))
	USE_FLASK_COMPRESS = int(environ.get('USE_FLASK_COMPRESS'))

	EMAIL_ERROR_REPORTS = int(environ.get('EMAIL_ERROR_REPORTS'))
	EMAIL_ERROR_REPORTS_ADDRESSES = json.loads(environ.get('EMAIL_ERROR_REPORTS_ADDRESSES'))

	COMPANY_NAME = environ.get('COMPANY_NAME')

	# # these two didn't work
	# STATIC_FOLDER = "/static"
	# STATIC_URL_PATH="/ls/static/"

	# SQLALCHEMY_DATABASE_URI = 'sqlite:///commerce.db'
	POSTGRES_DB_URI = {
	    'user': environ.get('POSTGRES_DB_USERNAME'),
	    'pw': environ.get('POSTGRES_DB_PASSWORD'),
	    'db': environ.get('POSTGRES_DB_DATABASE'),
	    'host': environ.get('POSTGRES_DB_HOST'),
	    'port': environ.get('POSTGRES_DB_PORT'),
	}
	SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_DB_URI
	SQLALCHEMY_ECHO = False
	# # Database bindings
	#
	# POSTGRES_TEST_DB_URI = {
	#     'user': environ.get('POSTGRES_TEST_DB_USERNAME'),
	#     'pw': environ.get('POSTGRES_TEST_DB_PASSWORD'),
	#     'db': environ.get('POSTGRES_TEST_DB_DATABASE'),
	#     'host': environ.get('POSTGRES_TEST_DB_HOST'),
	#     'port': environ.get('POSTGRES_TEST_DB_PORT'),
	# }
	#
	# SQLALCHEMY_TEST_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_TEST_DB_URI
	#
	# SQLALCHEMY_BINDS = {
	# 	'postgres_test': SQLALCHEMY_TEST_DATABASE_URI
	# }
	#
	# # / Database bindings /


	# # Sessions, Redis, Cache, Cookies
	if OS_TYPE != 'win32':
		SESSION_TYPE = environ.get('SESSION_TYPE')
		SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

	CACHE_TYPE = environ.get('CACHE_TYPE')
	CACHE_DEFAULT_TIMEOUT = 300
	CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
	# # / Sessions, Redis, Cache, Cookies /


	# modules url prefixes
	API_URL_PREFIX = environ.get('API_URL_PREFIX')
	COMMERCE_URL_PREFIX = environ.get('COMMERCE_URL_PREFIX')

	API_AND_ADMIN_ONLY = int(environ.get('API_AND_ADMIN_ONLY'))

	# works if commerce_url_prefix is null
	SHOW_LANDING_PAGE_ON_ROOT = int(environ.get('SHOW_LANDING_PAGE_ON_ROOT'))
	# / module url prefixes /

	# default language for session
	BABEL_DEFAULT_LOCALE = 'tk'

	# MAIL CONFIGURATION
	### testing ##
	MAIL_SUPPRESS_SEND = False
	MAIL_DEBUG = False
	### / testing /
	MAIL_SERVER = environ.get('MAIL_SERVER')
	MAIL_PORT = int(environ.get('MAIL_PORT'))
	MAIL_USE_TLS = True
	# MAIL_USE_SSL = False
	MAIL_USERNAME = environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
	# / MAIL CONFIGURATION /
	
	# #  Online Payment
	# URL for the service that will be used for payment check 
	PAYMENT_VALIDATION_SERVICE_URL = environ.get('PAYMENT_VALIDATION_SERVICE_URL')
	PAYMENT_VALIDATION_SERVICE_USERNAME = environ.get('PAYMENT_VALIDATION_SERVICE_USERNAME')
	PAYMENT_VALIDATION_SERVICE_PASSWORD = environ.get('PAYMENT_VALIDATION_SERVICE_PASSWORD')
	PAYMENT_VALIDATION_KEY = environ.get('PAYMENT_VALIDATION_KEY')
	PAYMENT_VALIDATION_VALUE = environ.get('PAYMENT_VALIDATION_VALUE')
	
	# # / Online Payment /


	# set to True if you want to use BCrypt hashing
	HASHED_PASSWORDS = False

	# # to give each api it's pagination:
	RESOURCES_PER_PAGE = 30
	INVOICES_PER_PAGE = 15
	API_OBJECTS_PER_PAGE = 10

	# REG_NO generator's random range
	REG_NUM_RANDOM_RANGE = 1000000000

	# # elasticsearch search engine's url
	# ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')

	# set to True if you want to sell resources
	# if no left in Res_total.ResPendingTotalAmount
	NEGATIVE_WH_QTY_SALE = False
	NEGATIVE_WH_QTY_ORDER = True

	# # ability to make an order if qty of resoruce
	# # is greater than Res_total in warehouse
	# OVERRIDE_WH_QTY_ORDER = True

	# set to True to show resources
	# if no left in Res_total.ResTotBalace
	SHOW_NEGATIVE_WH_QTY_RESOURCE = int(environ.get('SHOW_NEGATIVE_WH_QTY_RESOURCE'))

	# language and currency of price-to-text converter
	PRICE_2_TEXT_LANGUAGE = 'tk'
	# PRICE_2_TEXT_LANGUAGE = 'en'
	# PRICE_2_TEXT_LANGUAGE = 'ru'
	PRICE_2_TEXT_CURRENCY = 'TMT'
	# PRICE_2_TEXT_CURRENCY = 'USD'
	# PRICE_2_TEXT_CURRENCY = 'RUB'


	# IMAGES CONFIGURATION 
	# icon extentions and size
	ALLOWED_ICON_EXTENSIONS = set(['png','jpg','jpeg','svg'])
	ALLOWED_IMAGE_EXTENSIONS = set(['png','jpg','jpeg'])
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
	IMAGE_RANDOM_HEX_LENGTH = 14

	# Put a watermark layer on images
	# (esure existence in '/web_config/watermark.png')
	ADD_RESOURCE_WATERMARK = True

	# Rename images to the data given in image_name
	USE_PROVIDED_IMAGE_FILENAME = False
	
	# Types name of images to be written:
	# 1 = ResName
	# 2 = Barcode
	PROVIDED_IMAGE_FILENAME_TYPE = 1

	# Characters that are unable to use in FileName
	FILENAME_INVALID_CHARACTERS = ['/', '\\', '"', ':', '*', '?', '<', '>', '|']

	# Extention to be saved to while blob synch
	BLOB_TO_IMAGE_SAVE_EXT = "png"

	# / IMAGES CONFIGURATION /


	# cookies / security
	# SESSION_COOKIE_SECURE=True,
	# SESSION_COOKIE_HTTPONLY=True,
	# SESSION_COOKIE_SAMESITE='Lax'


	# VIEW AND ROUTES CONFIGURATION
	# put the route names to be used to access the pages
	COMMERCE_HOME_PAGE = "/commerce"
	COMMERCE_ABOUT_PAGE = "/about"
	COMMERCE_COLLECTION_VIEW = "/collection"
	COMMERCE_CONTACTS_PAGE = "/contact"

	COMMERCE_PROFILE_PAGE = "/profile"
	COMMERCE_PROFILE_EDIT_PAGE = "/profile_edit"
	COMMERCE_WISHLIST_PAGE = "/wishlist"
	COMMERCE_ORDERS_PAGE = "/orders"


	COMMERCE_CART_VIEW = "/cart"
	COMMERCE_LIST_VIEW = "/v-list"
	COMMERCE_GRID_VIEW = "/v-grid"
	COMMERCE_SEARCH_VIEW = "/search"
	COMMERCE_RESOURCE_VIEW = "/product"
	# / VIEW AND ROUTES CONFIGURATION /

	# view route titles configuration
	# Info to be displayed in html: <title>Home page</title>
	# set to None if dont want to display anything 
	COMMERCE_HOME_PAGE_TITLE = environ.get('COMMERCE_HOME_PAGE_TITLE') if environ.get('COMMERCE_HOME_PAGE_TITLE') else "Main"
	COMMERCE_ABOUT_PAGE_TITLE = "About us"
	COMMERCE_COLLECTION_VIEW_TITLE = "Collection"
	COMMERCE_CONTACTS_PAGE_TITLE = "Contact"

	COMMERCE_PROFILE_PAGE_TITLE = "Profile"
	COMMERCE_PROFILE_EDIT_PAGE_TITLE = "Edit profile"
	COMMERCE_WISHLIST_PAGE_TITLE = "Wishlist"
	COMMERCE_ORDERS_PAGE_TITLE = "Orders"

	COMMERCE_CART_VIEW_TITLE = "Cart"
	COMMERCE_LIST_VIEW_TITLE = "Category"
	COMMERCE_GRID_VIEW_TITLE = "Category"
	COMMERCE_SEARCH_VIEW_TITLE = "Search"
	COMMERCE_SORT_VIEW_TITLE = "Sort"

	# set to False if you want to use unique COMMERCE_RESOURCE_VIEW_TITLE
	RESOURCE_NAME_ON_TITLE = True
	COMMERCE_RESOURCE_VIEW_TITLE = "Product"
	# / view route titles configuration /

	# templates file location configuration
	COMMERCE_TEMPLATES_FOLDER_PATH = "/commerce/bee"
	# COMMERCE_TEMPLATES_FOLDER_PATH = "/commerce/main"
	
	COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH = "/commerce/admin"
	# / templates file location configuration /

	# tag resources as new if they exist **amount** days
	COMMERCE_RESOURCE_NEWNESS_DAYS = 10
	# how many resources to show in rating view
	TOP_RATED_RESOURCES_AMOUNT = 15
	FEATURED_RESOURCE_AMOUNT = 15
	RESOURCE_MAIN_PAGE_SHOW_QTY = 8
	SMALLEST_RATING_VALUE_SHOW = 3.5

	# location of robots.txt and sitemap.xml
	WEB_CONFIG_DIRECTORY = path.join("static", "web_config")