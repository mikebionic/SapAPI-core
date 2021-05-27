import requests
import json

from main_pack.config import Config


def do_mpi_gov_tm_payment_service_register_request(req):
	data = {}

	RegNo = req['RegNo']
	TotalPrice = int(round(float(req['TotalPrice']), 2) * 100)
	OrderDesc = req['OrderDesc']

	currency = 934
	language = "ru"

	register_url = Config.PAYMENT_VALIDATION_REGISTER_URL
	service_username = Config.PAYMENT_VALIDATION_SERVICE_USERNAME
	service_password = Config.PAYMENT_VALIDATION_SERVICE_PASSWORD

	returnUrl = f"https://mpi.gov.tm/payment/finish.html%3Flogin%3D{service_username}%26password%3D{service_password}&userName={service_username}&pageView=DESKTOP&description={OrderDesc}"
	payment_order_check_req_url = f"{register_url}orderNumber={RegNo}&currency={currency}&amount={TotalPrice}&language={language}&password={service_password}&returnUrl={returnUrl}"
	print(payment_order_check_req_url)

	try:
		r = requests.get(payment_order_check_req_url, verify=False)
		response_json = json.loads(r.text)
		print(response_json)
		if int(response_json["errorCode"]) != 0:
			raise Exception

		data = response_json
		data["RegNo"] = RegNo
		data["TotalPrice"] = TotalPrice
		data["OrderDesc"] = OrderDesc

	except Exception as ex:
		print(ex)

	return data