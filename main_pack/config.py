import sys

class Config:
	SECRET_KEY = 'jbvfr84iojnbv7oi-02933jndudm094jfo+_OygcuHUH'
	SYNCH_SHA = '''5jo8h2Rz+IpBvftYWrG8T3UxYAWwJM2d/+J2Wjh7qVcPrlKCOO6y0+m/Pm3jAAiz85IBi5qb4FwdlgRFKXG1397YVkwK+HwfoJrnJq/A3thjk189iB5bhxhNQrdPV3YU2DPOex1g5Gq2XGFrrIKo2mTM4YpYnWbk2wsj7OUvBgXdBKY2G70xdSJnJ/9uIC4y3IAkTlPKfh0+pTxbKfoJgw+gvNfLEDcT7e4UZw075QlwZNOrhxLg+KrK8WL8VdqBqDxMUvDivrcLFlMtiNUNoIN5MTW8otjRU1Eu76yMNvqJBAat2d1STBPPUAhHUk9cS6/rWj0nW7BKVndz1qrNTt+MxyqFg0phYYy+Ci0ul2ngjY0Up4X0T7TOnDAMROitQy3o1F4GkKn8xE7zFYu0KkQAxneBRS9HAromh4lnhk/sKKjqFrUjLKz/jQvCtOm/AZkR91p9ReGbKmEQKHYWJn1+X5fr2QheQsgI20DlSrUxhOsJUpar5rDKr/Mtnj50gl6r+YKF34MWvokCUF4coMuOugdOeWwcMV+vXheO1YrQM/OFEYEdgrdLT+U1ozZp8RIAjw7emuMZR49wwuyx6G5zTepZfhQG1ifTs2rdHayKWeRzqsmCSN39JXNJXeVp2mQxHOltD0osl6XuzRJD9wZn3YzIkTf8ENCjAX9Bz+eVM1SIlmnxLZdX1pPnlFZ9T6x3ybcDbrN4yDgadkjP42rEdTZGWyPEzOjGu4F4uvheeS5Vzq+UB1FAVU+g/v8Wy32pI1QBkRBTvxzfpl7I0GZpV3sqIbDXoWPrzX/1AVmkjkGT76A5Fc94FY7EB+/joO32UdlRSzBS28afgpBNT99r8tRyUTiI54AApe5lpDmVI6NLDWetbad0NX2vHHxrO4T83tsZfDYIwj4DLMAL+4SVwoGEof4beEYVt1CTeRT7kn7NFGlWyKyKhrFwnUTezTleiuMm4X3aNvMmHsQKdI0+eq9HRQW0fL1l1cUiLizSEJ0xFGUVmMi0qTL4gfHGo9+EuB2voijBb8ntO7yC8n5ZpkC70sxvejBojlcN+8FevK0sK13rkjWl1xPG0Ytg6y33QzQhjuhuA6W00ttosiqyBtVc+N2FVzhfF8WqGsx9Mewz/o4PoPsvZ2gJvqwKtnGtHjAb0QzNtWtxi52aFyem6v0A56eJOv351fdC27O+XIx8yF/+0tPQTh8gCEZcfNdKGdiGnbgnGgY7YqOpvaVpK2O6U2yCRQv+J3cdct6N1AI5urlcSOPhdHYAgnUG6HeGxNKCwYUXPbjmNZX6LdiCIrjDzm6B9X9qtM1DiQzn/V38EA3PMmPMcd1TTlGaaJzfbY5XvNua6J6XANOeVWOFfdJF/4ImEsolt26QBehwMn2Nsh53ElEz7WHjk2t75RnjU+LUqjhnSgQ+JogHab+7ZrsC5yIkek0YZcIsVGrpr3N1fsdB2pZtgPi4ngAWcAI8h1cQSYz7gvzOwht5ztKqfU5gLY5gYg3rJ2h2kGgPCHGbcvtlkCYdNsyPgXnEEp8qp83rG0KqumLU8h0KXJaSUpmUaOKfcw=='''
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

	# get OS Type to configure app for Windows or Linux
	OS_TYPE = sys.platform

	# set to True if you want to sell resources
	# if no left in Res_total  
	NEGATIVE_WH_QTY_SALE = False
	NEGATIVE_WH_QTY_ORDER = True

	# ability to make an order if qty of resoruce
	# is greater than Res_total in warehouse
	OWERRIDE_WH_QTY_ORDER = True

	# set to True to show resources
	# if no left in Res_total
	SHOW_NEGATIVE_WH_QTY_RESOURCE = True

	PRICE_2_TEXT_LANGUAGE = 'tk'
	# PRICE_2_TEXT_LANGUAGE = 'en'
	# PRICE_2_TEXT_LANGUAGE = 'ru'
	PRICE_2_TEXT_CURRENCY = 'TMT'
	# PRICE_2_TEXT_CURRENCY = 'USD'
	# PRICE_2_TEXT_CURRENCY = 'RUB'

	ALLOWED_ICON_EXTENSIONS = set(['png','jpg','jpeg','svg'])
	ALLOWED_IMAGE_EXTENSIONS = set(['png','jpg','jpeg'])
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
