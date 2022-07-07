
from datetime import datetime

from main_pack import db
from main_pack.models import Order_inv, Rp_acc

from .validate_halkbank_payment import validate_halkbank_payment
from .validate_InterActiv_payment import validate_InterActiv_payment
from main_pack.api.common import get_UserId_and_RpAccId_from_login_and_uuid_info

def validate_order_inv_payment(req, model_type, current_user):

	data = {}
	status = 0
	message = ''

	try:
		_, _, RpAccId, _, _ = get_UserId_and_RpAccId_from_login_and_uuid_info(
			model_type,
			current_user,
			req["RpAccGuid"] if "RpAccGuid" in req else None
		)

		if not RpAccId:
			message = "v1 validate order inv exception | no such rp acc"
			print(f"{datetime.now()} | {message}")
			raise Exception

		OInvRegNo = req["OInvRegNo"]
		OrderId = req["OrderId"]
		online_payment_type = req["online_payment_type"]

		if not OInvRegNo or not OrderId:
			message = "Payment Validation: failed (Reg no or OrderId is None)"
			print(f"{datetime.now()} | {message}")
			raise Exception(message)

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
					if online_payment_type == "halkbank":
						response_json, order_inv, message, status = validate_halkbank_payment(
							OrderId = OrderId,
							OrderInv_model = order_inv
						)

					if online_payment_type == "foreign_affairs_bank":
						response_json, order_inv, message, status = validate_InterActiv_payment(
							OrderId = OrderId,
							OrderInv_model = order_inv
						)

					order_inv.PaymCode = str(response_json)[:500]
					order_inv.PaymDesc = OrderId
					db.session.commit()
					data = response_json

				except Exception as ex:
					message = "Payment Validation: failed (Connection error)"
					print(f"{datetime.now()} | Payment Validation Exception: {ex}")

					req["message"] = message
					order_inv.PaymCode = str(req)[:500]
					order_inv.InvStatId = 14
					db.session.commit()

			else:
				message = "Payment successfully done!"

		else:
			message = "Payment Validation: failed, Order not found"
			print(f"{datetime.now()} | {message}")
	
	except Exception as ex:
		print(f"{datetime.now()} | v1 order validation exception: {ex}")
		
	return data, status, message