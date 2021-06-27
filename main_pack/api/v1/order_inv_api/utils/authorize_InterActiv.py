import requests
from datetime import datetime


def authorize_InterActiv(url, ClientId, ClientSecret):

	auth_headers = {
		"ClientId": ClientId,
		"ClientSecret": ClientSecret
	}

	auth_token = None
	try:
		r = requests.post(
			url,
			headers = auth_headers
		)

		if not r.headers:
			raise Exception

		if 'Authorization' not in r.headers:
			raise Exception
		
		auth_token = r.headers["Authorization"]

	except Exception as ex:
		print(f"{datetime.now()} InterActiv payment auth exception: {ex}")

	return auth_token
	