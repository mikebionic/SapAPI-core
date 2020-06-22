# -*- coding: utf-8 -*-
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

	# # to give each api it's pagination: 
	RESOURCES_PER_PAGE = 15
	API_OBJECTS_PER_PAGE = 10

	REG_NUM_RANDOM_RANGE = 10000

	ELASTICSEARCH_URL = 'http://localhost:9200'

	# OS_TYPE = 'windows'
	OS_TYPE = 'linux'
