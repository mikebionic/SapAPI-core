import requests
from datetime import datetime

from main_pack.config import Config
from .authorize_InterActiv import authorize_InterActiv



def do_InterActiv_payment_service_register_request():

	try:
		auth_token = authorize_InterActiv(
			url = Config.INTERACTIV_PAYMENT_SERVICE_URL,
			ClientId = Config.INTERACTIV_PAYMENT_CLIENTID,
			ClientSecret = Config.INTERACTIV_PAYMENT_CLIENTSECRET
		)

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment register exception: {ex}")