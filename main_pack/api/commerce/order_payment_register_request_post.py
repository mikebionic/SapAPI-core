import requests
import json
from flask import (
	make_response,
	jsonify,
	request,
)

from main_pack.config import Config
from . import api

@api.route("/order-payment-register-request/", methods=['POST'])
def order_payment_register_request_post():
	req = request.get_json()
	data = do_payment_register_request(req)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code

def do_payment_register_request(req):
	data = {}

	RegNo = req['RegNo']
	TotalPrice = int(round(float(req['TotalPrice']), 2) * 100)
	OrderDesc = req['OrderDesc']

	currency = 934
	language = "ru"

	register_url = Config.HALKBANK_PAYMENT_REGISTER_URL
	service_username = Config.HALKBANK_PAYMENT_SERVICE_USERNAME
	service_password = Config.HALKBANK_PAYMENT_SERVICE_PASSWORD

	returnUrl = f"https://mpi.gov.tm/payment/finish.html%3Flogin%3D{service_username}%26password%3D{service_password}&userName={service_username}&pageView=DESKTOP&description={OrderDesc}"
	payment_order_check_req_url = f"{register_url}orderNumber={RegNo}&currency={currency}&amount={TotalPrice}&language={language}&password={service_password}&returnUrl={returnUrl}"

	try:
		r = requests.get(payment_order_check_req_url, verify=False)
		response_json = json.loads(r.text)
		if int(response_json["errorCode"]) != 0:
			raise Exception

		data = response_json
		data["RegNo"] = RegNo
		data["TotalPrice"] = TotalPrice
		data["OrderDesc"] = OrderDesc

	except Exception as ex:
		print(ex)

	return data