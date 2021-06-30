
import requests
import json
from datetime import datetime

from main_pack.config import Config
from .authorize_InterActiv import authorize_InterActiv


def validate_InterActiv_payment(OrderId, OrderInv_model):
	response_json, OrderInv_model, message, status = {}, OrderInv_model, "", 0
	try:
		auth_token = authorize_InterActiv(
				url = Config.INTERACTIV_PAYMENT_SERVICE_URL,
				ClientId = Config.INTERACTIV_PAYMENT_CLIENTID,
				ClientSecret = Config.INTERACTIV_PAYMENT_CLIENTSECRET
			)
		if auth_token:
			r = requests.get(
				f"{Config.INTERACTIV_PAYMENT_VALIDATION_URL}/{OrderId}",
				headers = {"Authorization": auth_token},
				verify = False
			)
			response_json = r.json()

			if (response_json["response"][Config.INTERACTIV_PAYMENT_VALIDATION_KEY] == Config.INTERACTIV_PAYMENT_VALIDATION_VALUE):
				PaymentAmount = float(response_json["transaction"]["totalAmount"])
				OrderInv_model.OInvPaymAmount = PaymentAmount
				OrderInv_model.InvStatId = 1
				if (PaymentAmount >= OrderInv_model.OInvFTotal):
					OrderInv_model.PaymStatusId = 2
				elif (PaymentAmount < OrderInv_model.OInvFTotal and PaymentAmount > 0):
					OrderInv_model.PaymStatusId = 3
				message = "Payment Validation: success"
				status = 1

			else:
				# invoice status = "Payment fail"
				# Payment status = "Not paid"
				OrderInv_model.PaymStatusId = 1
				OrderInv_model.OInvPaymAmount = 0
				OrderInv_model.InvStatId = 14

				message = f"Payment Validation: failed (OrderStatus = { response_json['response']['operationResultDescription'] })"
				print(f"{datetime.now()} | {message}")

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment validation exception: {ex}")

	return response_json, OrderInv_model, message, status

