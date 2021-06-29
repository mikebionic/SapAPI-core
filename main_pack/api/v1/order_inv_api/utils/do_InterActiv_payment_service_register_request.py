import requests
from datetime import datetime

from main_pack.config import Config
from .authorize_InterActiv import authorize_InterActiv
from .initiate_order_InterActiv import initiate_order_InterActiv
from .generate_InterActiv_payload import generate_InterActiv_payload


def do_InterActiv_payment_service_register_request(
	req,
	return_url,
	CurrencyNumCode = None,
	CustomerName = None,
	CustomerEmail = None,
	CustomerHomePhone = None,
	CustomerMobilePhone = None,
	UserAgent = None,
	RemoteAddress = None,
	ScreenHeight = None,
	ScreenWidth = None,
):

	try:
		auth_token = authorize_InterActiv(
			url = Config.INTERACTIV_PAYMENT_SERVICE_URL,
			ClientId = Config.INTERACTIV_PAYMENT_CLIENTID,
			ClientSecret = Config.INTERACTIV_PAYMENT_CLIENTSECRET
		)
		if auth_token:
			payload_data = generate_InterActiv_payload(
				MerchantId = Config.INTERACTIV_PAYMENT_MERCHANTID,
				TerminalId = Config.INTERACTIV_PAYMENT_TERMINALID,
				return_url = return_url,
				CurrencyNumCode = CurrencyNumCode,
				CustomerName = CustomerName,
				CustomerEmail = CustomerEmail,
				CustomerHomePhone = CustomerHomePhone,
				CustomerMobilePhone = CustomerMobilePhone,
				UserAgent = UserAgent,
				RemoteAddress = RemoteAddress,
				ScreenHeight = ScreenHeight,
				ScreenWidth = ScreenWidth,
			)

			result = initiate_order_InterActiv(
				Config.INTERACTIV_PAYMENT_SERVICE_URL,
				auth_token,
				payload_data
			)

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment register exception: {ex}")