class Config:
	SECRET_KEY = 'jbvfr84iojnbv7oi-02933jndudm094jfo+_OygcuHUH'
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///commerce.db'

	POSTGRES = {
	    'user': 'postgres',
	    'pw': 'd152535k',
	    'db': 'dbSapHasapNewNew',
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
