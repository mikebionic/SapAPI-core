
from flask import(
	json,
)
import requests
from datetime import datetime

from main_pack import db
from main_pack.config import Config
from main_pack.models import Order_inv, Rp_acc


def validate_order_inv_payment(req, model_type, current_user):

	data = {}
	status = 0
	message = ''

	try:
		if model_type == "rp_acc":
			RpAccId = current_user.RpAccId

		else:
			RpAccGuid = req['RpAccGuid']
			rp_acc = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
			RpAccId = rp_acc.RpAccId if rp_acc else None
			if not RpAccId:
				message = "v1 validate order inv exception | no such rp acc"
				print(f"{datetime.now()} | {message}")
				raise Exception

		OInvRegNo = req["OInvRegNo"]
		OrderId = req["OrderId"]

		if not OInvRegNo or not OrderId:
			message = "Payment Validation: failed (Reg no or OrderId is None)"
			print(f"{datetime.now()} | {message}")
			raise Exception

		order_inv = Order_inv.query\
			.filter_by(
				RpAccId = RpAccId,
				OInvRegNo = OInvRegNo,
				GCRecord = None)\
			.first()

		if order_inv:
			# if order isn't already paid
			if order_inv.PaymStatusId != 2:
				try:
					r = requests.get(f"{Config.HALKBANK_PAYMENT_SERVICE_URL}?orderId={OrderId}&password={Config.HALKBANK_PAYMENT_SERVICE_PASSWORD}&userName={Config.HALKBANK_PAYMENT_SERVICE_USERNAME}", verify=False)
					response_json = json.loads(r.text)

					if (str(response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]) == str(Config.HALKBANK_PAYMENT_VALIDATION_VALUE)):
						PaymentAmount = int(response_json["Amount"])/100
						order_inv.OInvPaymAmount = PaymentAmount
						order_inv.InvStatId = 1
						if (PaymentAmount >= order_inv.OInvFTotal):
							order_inv.PaymStatusId = 2
						elif (PaymentAmount < order_inv.OInvFTotal and PaymentAmount > 0):
							order_inv.PaymStatusId = 3
						message = "Payment Validation: success"
						status = 1

					else:
						# invoice status = "Payment fail"
						# Payment status = "Not paid"
						order_inv.PaymStatusId = 1
						order_inv.OInvPaymAmount = 0
						order_inv.InvStatId = 14

						message = f"Payment Validation: failed (OrderStatus = {response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]})"
						print(f"{datetime.now()} | {message}")

					order_inv.PaymCode = str(response_json)
					order_inv.PaymDesc = OrderId
					db.session.commit()
					data = response_json

				except Exception as ex:
					message = "Payment Validation: failed (Connection error)"
					print(f"{datetime.now()} | Payment Validation Exception: {ex}")

					req["message"] = message
					order_inv.PaymCode = str(req)
					order_inv.InvStatId = 14
					db.session.commit()

			else:
				message = "Payment successfully done!"

		else:
			message = "Payment Validation: failed (Order_inv is None)"
			print(f"{datetime.now()} | {message}")
	
	except Exception as ex:
		print(f"{datetime.now()} | v1 order validation exception: {ex}")
		
	return data, status, message