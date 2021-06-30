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
	data = {}

	OInvRegNo = req['OInvRegNo']
	TotalPrice = float(req['TotalPrice'])
	OrderDesc = req['OrderDesc']

	try:
		auth_token = authorize_InterActiv(
			url = Config.INTERACTIV_PAYMENT_SERVICE_URL,
			ClientId = Config.INTERACTIV_PAYMENT_CLIENTID,
			ClientSecret = Config.INTERACTIV_PAYMENT_CLIENTSECRET
		)
		if auth_token:
			InterActiv_args = {
				"MerchantId": Config.INTERACTIV_PAYMENT_MERCHANTID,
				"TerminalId": Config.INTERACTIV_PAYMENT_TERMINALID,
				"TotalPrice": TotalPrice,
				"OInvRegNo": OInvRegNo,
				"OrderDesc": OrderDesc,
				"return_url": return_url,
				"CurrencyNumCode": CurrencyNumCode,
				"CustomerName": CustomerName,
				"CustomerEmail": CustomerEmail,
				"CustomerHomePhone": CustomerHomePhone,
				"CustomerMobilePhone": CustomerMobilePhone,
				"UserAgent": str(UserAgent)[:2000],
				"RemoteAddress": str(RemoteAddress)
			}

			if ScreenHeight:
				InterActiv_args["ScreenHeight"] = ScreenHeight
			if ScreenWidth:
				InterActiv_args["ScreenWidth"] = ScreenWidth

			payload_data = generate_InterActiv_payload(**InterActiv_args)
			data = initiate_order_InterActiv(
				Config.INTERACTIV_PAYMENT_SERVICE_URL,
				auth_token,
				payload_data
			)

			if not data:
				raise Exception

			# if (data["response"][Config.INTERACTIV_PAYMENT_VALIDATION_KEY] != "OPG-00100"):
			# 	raise Exception

			data["RegNo"] = OInvRegNo
			data["OInvRegNo"] = OInvRegNo
			data["TotalPrice"] = TotalPrice
			data["OrderDesc"] = OrderDesc
			data["OrderId"] = data["response"]["orderId"]
			data["checkout_url"] = data["_links"]["redirectToCheckout"]["href"]
			data["online_payment_type"] = req["online_payment_type"] if "online_payment_type" in req else "halkbank"

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment register exception: {ex}")

	return data