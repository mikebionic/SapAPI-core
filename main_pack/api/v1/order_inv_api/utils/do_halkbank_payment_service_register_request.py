from flask.helpers import url_for
import requests
import json
from datetime import datetime

from main_pack import db
from main_pack.config import Config
from main_pack.models import Order_inv


def do_halkbank_payment_service_register_request(req, return_url=None):
	data = {}

	RegNo = req['OInvRegNo']
	TotalPrice = int(round(float(req['TotalPrice']), 2) * 100)
	OrderDesc = req['OrderDesc']

	currency = 934
	language = "ru"

	register_url = Config.PAYMENT_VALIDATION_REGISTER_URL
	service_username = Config.PAYMENT_VALIDATION_SERVICE_USERNAME
	service_password = Config.PAYMENT_VALIDATION_SERVICE_PASSWORD

	default_return_url = f"https://mpi.gov.tm/payment/finish.html%3Flogin%3D{service_username}%26password%3D{service_password}&userName={service_username}&pageView=DESKTOP&description={OrderDesc}"
	payment_return_url = f"{return_url}%3Flogin%3D{service_username}%26password%3D{service_password}&userName={service_username}&pageView=DESKTOP&description={OrderDesc}" if return_url else default_return_url
	payment_order_check_req_url = f"{register_url}orderNumber={RegNo}&currency={currency}&amount={TotalPrice}&language={language}&password={service_password}&returnUrl={payment_return_url}&failUrl={payment_return_url}"

	try:
		r = requests.get(payment_order_check_req_url, verify=False)
		response_json = json.loads(r.text)

		errorCode = int(response_json["errorCode"])
		if not (errorCode == 0 or errorCode == 1):
			print(f"errorcode {errorCode}")
			raise Exception

		# if last regNo request already registered
		if int(response_json['errorCode']) == 1:
			new_RegNo = str(datetime.now().timestamp())
			RegNo = update_order_RegNo(RegNo, new_RegNo)

			payment_order_check_req_url = f"{register_url}orderNumber={RegNo}&currency={currency}&amount={TotalPrice}&language={language}&password={service_password}&returnUrl={payment_return_url}&failUrl={payment_return_url}"

			r = requests.get(payment_order_check_req_url, verify=False)
			response_json = json.loads(r.text)

			if int(response_json["errorCode"]) != 0:
				raise Exception

		data = response_json
		data["RegNo"] = RegNo
		data["OInvRegNo"] = RegNo
		data["TotalPrice"] = TotalPrice
		data["OrderDesc"] = OrderDesc

	except Exception as ex:
		print(f"{datetime.now()} | mpi.gov.tm payment register Exception: {ex}")

	return data


def update_order_RegNo(RegNo, new_RegNo):
	try:
		order = Order_inv.query.filter_by(OInvRegNo = RegNo).first()
		if order:
			order.OInvRegNo = new_RegNo
			db.session.commit()
			RegNo = order.OInvRegNo

	except Exception as ex:
		print(f"{datetime.now()} | order RegNo update Exception: {ex}")
	
	return RegNo