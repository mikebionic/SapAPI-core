import requests
from datetime import datetime
from main_pack.config import Config
import json

from main_pack.models import Db_inf


def make_register_request(payload):
	data = {}
	database = Db_inf.query.first()
	payload["DbInfGuid"] = str(database.DbInfGuid) if database else None

	try:
		r = requests.post(
			f"{Config.SAP_SERVICE_URL}{Config.SAP_SERVICE_URL_PREFIX}/devices/register/",
			data = json.dumps(payload),
			headers = {
				'Content-Type': 'application/json',
				'x-access-token': Config.SAP_SERVICE_KEY})

		server_response = r.json()

		if (r.status_code == 200 or r.status_code == 201):
			if server_response["status"] != 0:
				data = server_response["data"]

	except Exception as ex:
		print(f"{datetime.now()} | Device register response json Exception: {ex}")

	
	return data