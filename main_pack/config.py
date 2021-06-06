import sys
import redis
import json
import urllib
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
	APP_WEB_KEY = environ.get('APP_WEB_KEY')

	MAIN_CGUID = environ.get('MAIN_CGUID')
	C_MAIN_DIVGUID = environ.get('C_MAIN_DIVGUID')
	C_REGISTRATION_DIVGUID = environ.get('C_REGISTRATION_DIVGUID')

	SAP_SERVICE_KEY = environ.get('SAP_SERVICE_KEY')
	SAP_SERVICE_URL = environ.get('SAP_SERVICE_URL')
	SAP_SERVICE_URL_PREFIX = environ.get('SAP_SERVICE_URL_PREFIX')
	USE_ACTIVATION_CUSTOMER = int(environ.get('USE_ACTIVATION_CUSTOMER')) if environ.get('USE_ACTIVATION_CUSTOMER') else 0
	USE_ACTIVATION_SERVER = int(environ.get('USE_ACTIVATION_SERVER')) if environ.get('USE_ACTIVATION_SERVER') else 0
	USE_SERVERLESS_ACTIVATION = int(environ.get('USE_SERVERLESS_ACTIVATION')) if environ.get('USE_SERVERLESS_ACTIVATION') else 0
	BASE_32_FERNET_KEY = environ.get('BASE_32_FERNET_KEY')
	DEVICE_ALLOWED_TIMEOUT_DAYS = int(environ.get('DEVICE_ALLOWED_TIMEOUT_DAYS')) if environ.get('DEVICE_ALLOWED_TIMEOUT_DAYS') else 0

	# set to production if Production
	FLASK_ENV = 'development'

	# set to false to turn off debugging
	DEBUG = int(environ.get('DEBUG')) if environ.get('DEBUG') else 1
	TESTING = int(environ.get('TESTING')) if environ.get('TESTING') else 1

	USE_FLASK_CORS = int(environ.get('USE_FLASK_CORS')) if environ.get('USE_FLASK_CORS') else 1
	USE_FLASK_COMPRESS = int(environ.get('USE_FLASK_COMPRESS')) if environ.get('USE_FLASK_COMPRESS') else 1
	MINIFY_HTML_RESPONSE = int(environ.get('MINIFY_HTML_RESPONSE')) if environ.get('MINIFY_HTML_RESPONSE') else 1

	EMAIL_ERROR_REPORTS = int(environ.get('EMAIL_ERROR_REPORTS')) if environ.get('EMAIL_ERROR_REPORTS') else 0
	EMAIL_ERROR_REPORTS_ADDRESSES = json.loads(environ.get('EMAIL_ERROR_REPORTS_ADDRESSES')) or []

	COMPANY_NAME = environ.get('COMPANY_NAME') or 'Company'

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
	SQLALCHEMY_ECHO = int(environ.get('SQLALCHEMY_ECHO')) if environ.get('SQLALCHEMY_ECHO') else 0
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

	# # MSSQL binding
	# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:123456@192.168.31.77:1433/dbSapHasap?driver=ODBC+Driver+17+for+SQL+Server?TrustedConnection=yes'


	# # Sessions, Redis, Cache, Cookies
	if OS_TYPE != 'win32':
		SESSION_TYPE = environ.get('SESSION_TYPE')
		SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS')) if environ.get('SESSION_REDIS') else redis.from_url('redis://:@127.0.0.1:6379/1')

	CACHE_TYPE = environ.get('CACHE_TYPE') or ''
	CACHE_DEFAULT_TIMEOUT = 300
	DB_CACHE_TIME = int(environ.get('DB_CACHE_TIME')) if environ.get('DB_CACHE_TIME') else 600
	CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL') or 'redis://:@127.0.0.1:6379/2'
	# # / Sessions, Redis, Cache, Cookies /

	CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL') or 'redis://:@127.0.0.1:6379/3'
	CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND') or 'redis://:@127.0.0.1:6379/3'

	# modules url prefixes
	API_URL_PREFIX = environ.get('API_URL_PREFIX') or '/api'
	COMMERCE_URL_PREFIX = environ.get('COMMERCE_URL_PREFIX') or ''
	COMMERCE_ADMIN_URL_PREFIX = environ.get('COMMERCE_ADMIN_URL_PREFIX') or ''

	API_AND_ADMIN_ONLY = int(environ.get('API_AND_ADMIN_ONLY')) if environ.get('API_AND_ADMIN_ONLY') else 0

	# works if commerce_url_prefix is null
	SHOW_LANDING_PAGE_ON_ROOT = int(environ.get('SHOW_LANDING_PAGE_ON_ROOT')) if environ.get('SHOW_LANDING_PAGE_ON_ROOT') else 0
	# / module url prefixes /

	# default language for session
	BABEL_DEFAULT_LOCALE = 'tk'

	# MAIL CONFIGURATION
	### testing ##
	MAIL_SUPPRESS_SEND = False
	MAIL_DEBUG = False
	### / testing /
	MAIL_SERVER = environ.get('MAIL_SERVER')
	MAIL_PORT = int(environ.get('MAIL_PORT')) if environ.get('MAIL_PORT') else 587
	MAIL_USE_TLS = int(environ.get('MAIL_USE_TLS')) if environ.get('MAIL_USE_TLS') else 0
	MAIL_USE_SSL = int(environ.get('MAIL_USE_SSL')) if environ.get('MAIL_USE_SSL') else 0
	MAIL_USERNAME = environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
	COMPANY_MAIL = environ.get('COMPANY_MAIL') or environ.get('MAIL_USERNAME')
	# / MAIL CONFIGURATION /

	# #  Online Payment
	# URL for the service that will be used for payment check
	ALLOW_PAYMENT_INFO_API = int(environ.get('ALLOW_PAYMENT_INFO_API')) if environ.get('ALLOW_PAYMENT_INFO_API') else 1
	PAYMENT_VALIDATION_SERVICE_URL = environ.get('PAYMENT_VALIDATION_SERVICE_URL')
	PAYMENT_VALIDATION_REGISTER_URL = environ.get('PAYMENT_VALIDATION_REGISTER_URL')
	PAYMENT_VALIDATION_SERVICE_USERNAME = environ.get('PAYMENT_VALIDATION_SERVICE_USERNAME')
	PAYMENT_VALIDATION_SERVICE_PASSWORD = environ.get('PAYMENT_VALIDATION_SERVICE_PASSWORD')
	PAYMENT_VALIDATION_KEY = environ.get('PAYMENT_VALIDATION_KEY')
	PAYMENT_VALIDATION_VALUE = environ.get('PAYMENT_VALIDATION_VALUE')

	# # / Online Payment /


	# set to True if you want to use BCrypt hashing
	HASHED_PASSWORDS = int(environ.get('HASHED_PASSWORDS')) if environ.get('HASHED_PASSWORDS') else 0

	TOKEN_EXP_TIME_MINUTES = int(environ.get('TOKEN_EXP_TIME_MINUTES')) if environ.get('TOKEN_EXP_TIME_MINUTES') else 30

	# # to give each api it's pagination:
	RESOURCES_PER_PAGE = int(environ.get('RESOURCES_PER_PAGE')) if environ.get('RESOURCES_PER_PAGE') else 30
	INVOICES_PER_PAGE = int(environ.get('INVOICES_PER_PAGE')) if environ.get('INVOICES_PER_PAGE') else 30
	API_OBJECTS_PER_PAGE = int(environ.get('API_OBJECTS_PER_PAGE')) if environ.get('API_OBJECTS_PER_PAGE') else 20

	# REG_NO generator's random range
	REG_NUM_RANDOM_RANGE = int(environ.get('REG_NUM_RANDOM_RANGE')) if environ.get('REG_NUM_RANDOM_RANGE') else 1000000000

	# # elasticsearch search engine's url
	# ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')

	# set to True if you want to sell resources
	# if no left in Res_total.ResPendingTotalAmount
	NEGATIVE_WH_QTY_SALE = int(environ.get('NEGATIVE_WH_QTY_SALE')) if environ.get('NEGATIVE_WH_QTY_SALE') else 0
	NEGATIVE_WH_QTY_ORDER = int(environ.get('NEGATIVE_WH_QTY_ORDER')) if environ.get('NEGATIVE_WH_QTY_ORDER') else 1

	# # ability to make an order if qty of resoruce
	# # is greater than Res_total in warehouse
	# OVERRIDE_WH_QTY_ORDER = True

	# set to True to show resources
	# if no left in Res_total.ResTotBalace
	SHOW_NEGATIVE_WH_QTY_RESOURCE = int(environ.get('SHOW_NEGATIVE_WH_QTY_RESOURCE')) if environ.get('SHOW_NEGATIVE_WH_QTY_RESOURCE') else 0
	SHOW_NULL_RESOURCE_CATEGORY = int(environ.get('SHOW_NULL_RESOURCE_CATEGORY')) if environ.get('SHOW_NULL_RESOURCE_CATEGORY') else 1
	SEARCH_BY_RESOURCE_DESCRIPTION = int(environ.get('SEARCH_BY_RESOURCE_DESCRIPTION')) if environ.get('SEARCH_BY_RESOURCE_DESCRIPTION') else 1
	SHOW_ONLY_VALIDATED_RATING = 1

	MAIN_CURRENCY_CODE = environ.get('MAIN_CURRENCY_CODE') or 'TMT'
	DEFAULT_VIEW_CURRENCY_CODE = environ.get('DEFAULT_VIEW_CURRENCY_CODE') or 'TMT'
	DEFAULT_RES_PRICE_GROUP_ID = int(environ.get('DEFAULT_RES_PRICE_GROUP_ID')) if environ.get('DEFAULT_RES_PRICE_GROUP_ID') else 0
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
	ADD_RESOURCE_WATERMARK = int(environ.get('ADD_RESOURCE_WATERMARK')) if environ.get('ADD_RESOURCE_WATERMARK') else 0

	# Rename images to the data given in image_name
	USE_PROVIDED_IMAGE_FILENAME = int(environ.get('USE_PROVIDED_IMAGE_FILENAME')) if environ.get('USE_PROVIDED_IMAGE_FILENAME') else 0

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
	COMMERCE_HOME_PAGE = environ.get('COMMERCE_HOME_PAGE') or "/commerce/"
	COMMERCE_ABOUT_PAGE = environ.get('COMMERCE_ABOUT_PAGE') or "/about"
	COMMERCE_COLLECTION_VIEW = environ.get('COMMERCE_COLLECTION_VIEW') or "/collection"
	COMMERCE_CONTACTS_PAGE = environ.get('COMMERCE_CONTACTS_PAGE') or "/contact"

	COMMERCE_PROFILE_PAGE = environ.get('COMMERCE_PROFILE_PAGE') or "/profile"
	COMMERCE_PROFILE_EDIT_PAGE = environ.get('COMMERCE_PROFILE_EDIT_PAGE') or "/profile_edit"
	COMMERCE_WISHLIST_PAGE = environ.get('COMMERCE_WISHLIST_PAGE') or "/wishlist"
	COMMERCE_ORDERS_PAGE = environ.get('COMMERCE_ORDERS_PAGE') or "/orders"


	COMMERCE_CART_VIEW = environ.get('COMMERCE_CART_VIEW') or "/cart"
	COMMERCE_LIST_VIEW = environ.get('COMMERCE_LIST_VIEW') or "/v-list"
	COMMERCE_GRID_VIEW = environ.get('COMMERCE_GRID_VIEW') or "/v-grid"
	COMMERCE_SEARCH_VIEW = environ.get('COMMERCE_SEARCH_VIEW') or "/search"
	COMMERCE_RESOURCE_VIEW = environ.get('COMMERCE_RESOURCE_VIEW') or "/product"
	COMMERCE_BRANDS_PAGE = environ.get('COMMERCE_BRANDS_PAGE') or "/brands"
	# / VIEW AND ROUTES CONFIGURATION /

	# view route titles configuration
	# Info to be displayed in html: <title>Home page</title>
	# set to None if dont want to display anything
	COMMERCE_HOME_PAGE_TITLE = environ.get('COMMERCE_HOME_PAGE_TITLE') or "Main"
	COMMERCE_ABOUT_PAGE_TITLE = environ.get('COMMERCE_ABOUT_PAGE_TITLE') or "About us"
	COMMERCE_COLLECTION_VIEW_TITLE = environ.get('COMMERCE_COLLECTION_VIEW_TITLE') or "Collection"
	COMMERCE_CONTACTS_PAGE_TITLE = environ.get('COMMERCE_CONTACTS_PAGE_TITLE') or "Contact"
	COMMERCE_BRANDS_PAGE_TITLE = environ.get('COMMERCE_BRANDS_PAGE_TITLE') or "Brands"

	COMMERCE_PROFILE_PAGE_TITLE = environ.get('COMMERCE_PROFILE_PAGE_TITLE') or "Profile"
	COMMERCE_PROFILE_EDIT_PAGE_TITLE = environ.get('COMMERCE_PROFILE_EDIT_PAGE_TITLE') or "Edit profile"
	COMMERCE_WISHLIST_PAGE_TITLE = environ.get('COMMERCE_WISHLIST_PAGE_TITLE') or "Wishlist"
	COMMERCE_ORDERS_PAGE_TITLE = environ.get('COMMERCE_ORDERS_PAGE_TITLE') or "Orders"

	COMMERCE_CART_VIEW_TITLE = environ.get('COMMERCE_CART_VIEW_TITLE') or "Cart"
	COMMERCE_LIST_VIEW_TITLE = environ.get('COMMERCE_LIST_VIEW_TITLE') or "Category"
	COMMERCE_GRID_VIEW_TITLE = environ.get('COMMERCE_GRID_VIEW_TITLE') or "Category"
	COMMERCE_SEARCH_VIEW_TITLE = environ.get('COMMERCE_SEARCH_VIEW_TITLE') or "Search"
	COMMERCE_SORT_VIEW_TITLE = environ.get('COMMERCE_SORT_VIEW_TITLE') or "Sort"

	# set to False if you want to use unique COMMERCE_RESOURCE_VIEW_TITLE
	RESOURCE_NAME_ON_TITLE = int(environ.get('RESOURCE_NAME_ON_TITLE')) if environ.get('RESOURCE_NAME_ON_TITLE') else 1
	COMMERCE_RESOURCE_VIEW_TITLE = environ.get('COMMERCE_RESOURCE_VIEW_TITLE') or "Product"
	# / view route titles configuration /

	COMMERCE_SHOW_BRANDS_ON_RESOURCES_PAGE = int(environ.get('COMMERCE_SHOW_BRANDS_ON_RESOURCES_PAGE')) if environ.get('COMMERCE_SHOW_BRANDS_ON_RESOURCES_PAGE') else 0

	# templates file location configuration
	COMMERCE_TEMPLATES_FOLDER_PATH = environ.get("COMMERCE_TEMPLATES_FOLDER_PATH") or "/commerce/bee"
	# COMMERCE_TEMPLATES_FOLDER_PATH = "/commerce/bee"
	# COMMERCE_TEMPLATES_FOLDER_PATH = "/commerce/main"
	# COMMERCE_TEMPLATES_FOLDER_PATH = "/commerce/testing"

	COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH = environ.get("COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH") or "/commerce/admin"
	# / templates file location configuration /

	# tag resources as new if they exist **amount** days
	COMMERCE_RESOURCE_NEWNESS_DAYS = int(environ.get('COMMERCE_RESOURCE_NEWNESS_DAYS')) if environ.get('COMMERCE_RESOURCE_NEWNESS_DAYS') else 15
	# how many resources to show in rating view
	TOP_RATED_RESOURCES_AMOUNT = int(environ.get('TOP_RATED_RESOURCES_AMOUNT')) if environ.get('TOP_RATED_RESOURCES_AMOUNT') else 14
	FEATURED_RESOURCE_AMOUNT = int(environ.get('FEATURED_RESOURCE_AMOUNT')) if environ.get('FEATURED_RESOURCE_AMOUNT') else 14
	RESOURCE_MAIN_PAGE_SHOW_QTY = int(environ.get('RESOURCE_MAIN_PAGE_SHOW_QTY')) if environ.get('RESOURCE_MAIN_PAGE_SHOW_QTY') else 24
	SMALLEST_RATING_VALUE_SHOW = int(environ.get('SMALLEST_RATING_VALUE_SHOW')) if environ.get('SMALLEST_RATING_VALUE_SHOW') else 3.5

	# location of robots.txt and sitemap.xml
	WEB_CONFIG_DIRECTORY = path.join("static", "web_config")
	GOOGLE_ANALYTICS_TAG = environ.get('GOOGLE_ANALYTICS_TAG') or ''

	COMMERCE_ABOUT_DESCRIPTION = environ.get('COMMERCE_ABOUT_DESCRIPTION') or ''