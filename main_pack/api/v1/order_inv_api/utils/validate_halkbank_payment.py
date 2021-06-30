import requests
from flask import json
from datetime import datetime

from main_pack.config import Config


def validate_halkbank_payment(OrderId, OrderInv_model):
	response_json, OrderInv_model, message, status = {}, OrderInv_model, "", 0
	try:
		r = requests.get(f"{Config.HALKBANK_PAYMENT_SERVICE_URL}?orderId={OrderId}&password={Config.HALKBANK_PAYMENT_SERVICE_PASSWORD}&userName={Config.HALKBANK_PAYMENT_SERVICE_USERNAME}", verify=False)
		response_json = json.loads(r.text)

		if (str(response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]) == str(Config.HALKBANK_PAYMENT_VALIDATION_VALUE)):
			PaymentAmount = int(response_json["Amount"])/100
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

			message = f"Payment Validation: failed (OrderStatus = {response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]})"
			print(f"{datetime.now()} | {message}")
	
	except Exception as ex:
		print(f"{datetime.now()} Halkbank payment validation exception: {ex}")
	
	return response_json, OrderInv_model, message, status