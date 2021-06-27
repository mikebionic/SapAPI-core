import requests
from datetime import datetime

from main_pack.config import Config
from .authorize_InterActiv import authorize_InterActiv



def do_InterActiv_payment_service_register_request():
	# Get from config file
	# url
	# ClientId
	# ClientSecret
	# add config that checks if it may use interactiv
	try:
		auth_token = authorize_InterActiv(url, ClientId, ClientSecret)

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment register exception: {ex}")