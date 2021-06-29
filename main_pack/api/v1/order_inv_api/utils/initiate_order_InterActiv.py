import requests
import json
from datetime import datetime


def initiate_order_InterActiv(url, token, data):
	req_headers = {
		"Authorization": token,
		"Content-Type": "application/json",
		"Accept": "application/hal+json"
	}

	res = None
	try:
		r = requests.post(
			url,
			data = json.dumps(data),
			headers = req_headers
		)
		res = r
	except Exception as ex:
		print(f"{datetime.now()} InterActiv Order initiate exception: {ex}")

	return res