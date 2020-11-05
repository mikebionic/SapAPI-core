import sys
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
	SECRET_KEY = environ.get('SECRET_KEY')
	SYNCH_SHA = environ.get('SYNCH_SHA')
	C_MAIN_DIVGUID = environ.get('C_MAIN_DIVGUID')
	MAIN_CGUID = environ.get('MAIN_CGUID')
	# set to production if Production
	FLASK_ENV = 'development'
	# set to false to turn off debugging
	DEBUG = True
	TESTING = True

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

	# modules url prefixes
	API_URL_PREFIX = '/ls/api/'
	COMMERCE_URL_PREFIX = '/commerce'
	# / module url prefixes /

	# default language for session
	BABEL_DEFAULT_LOCALE = 'tk'

	# MAIL CONFIGURATION
	### testing ##
	MAIL_SUPPRESS_SEND = False
	# MAIL_DEBUG = True
	### / testing /
	MAIL_SERVER = environ.get('MAIL_SERVER')
	MAIL_PORT = environ.get('MAIL_PORT')
	MAIL_USE_TLS = True
	MAIL_USERNAME = environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
	# / MAIL CONFIGURATION /
	
	# #  Online Payment
	# URL for the service that will be used for payment check 
	ORDER_VALIDATION_SERVICE_URL = environ.get('ORDER_VALIDATION_SERVICE_URL')
	ORDER_VALIDATION_SERVICE_USERNAME = environ.get('ORDER_VALIDATION_SERVICE_USERNAME')
	ORDER_VALIDATION_SERVICE_PASSWORD = environ.get('ORDER_VALIDATION_SERVICE_PASSWORD')
	ORDER_VALIDATION_KEY = environ.get('ORDER_VALIDATION_KEY')
	ORDER_VALIDATION_VALUE = environ.get('ORDER_VALIDATION_VALUE')
	
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
	SHOW_NEGATIVE_WH_QTY_RESOURCE = False

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
	IMAGE_RANDOM_HEX_LENGTH = 14
	ADD_RESOURCE_WATERMARK = True

	# Extention to be saved to while blob synch
	BLOB_TO_IMAGE_SAVE_EXT = "png"

	# cookies / security
	# SESSION_COOKIE_SECURE=True,
	# SESSION_COOKIE_HTTPONLY=True,
	# SESSION_COOKIE_SAMESITE='Lax'

	# view routes naming configuration
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
	# / view routes naming configuration /

	# view route titles configuration
	# Info to be displayed in html: <title>Home page</title>
	# set to None if dont want to display anything 
	COMMERCE_HOME_PAGE_TITLE = None
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