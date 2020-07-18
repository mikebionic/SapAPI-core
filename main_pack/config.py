import sys

class Config:
	SECRET_KEY = 'jbvfr84iojnbv7oi-02933jndudm094jfo+_OygcuHUH'
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///commerce.db'

	POSTGRES = {
	    'user': 'postgres',
	    'pw': 'd152535k',
	    'db': 'dbSapHasap',
	    'host': 'localhost',
	    'port': '5432',
	}
	SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

	BABEL_DEFAULT_LOCALE = 'tk'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	# MAIL_USERNAME = os.environ.get('EMAIL_USER')
	# MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	MAIL_USERNAME = 'teamofbionics@gmail.com'
	MAIL_PASSWORD = 'bionics12345'

	# set to True if you want to use BCrypt hashing
	HASHED_PASSWORDS = False

	# # to give each api it's pagination: 
	RESOURCES_PER_PAGE = 15
	API_OBJECTS_PER_PAGE = 10

	REG_NUM_RANDOM_RANGE = 10000

	ELASTICSEARCH_URL = 'http://localhost:9200'

	OS_TYPE = sys.platform
	# set to True if you want to sell product
	# if no left in Res_total  
	NEGATIVE_WH_QTY_SALE = False
	NEGATIVE_WH_QTY_ORDER = True

	PRICE_2_TEXT_LANGUAGE = 'tk'
	# PRICE_2_TEXT_LANGUAGE = 'en'
	# PRICE_2_TEXT_LANGUAGE = 'ru'
	PRICE_2_TEXT_CURRENCY = 'TMT'
	# PRICE_2_TEXT_CURRENCY = 'USD'
	# PRICE_2_TEXT_CURRENCY = 'RUB'

	ALLOWED_ICON_EXTENSIONS = set(['png','jpg','jpeg','svg'])
	ALLOWED_IMAGE_EXTENSIONS = set(['png','jpg','jpeg'])
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024