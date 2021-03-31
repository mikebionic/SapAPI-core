from flask import jsonify, request, make_response
import json
import requests
from datetime import datetime

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.api.users.utils import addDeviceDict
from main_pack.api.base.validators import request_is_json
from main_pack.models import Device
from main_pack.models.base.models import Db_inf


@api.route("/devices/register/",methods=["POST"])
@request_is_json(request)
def register_device():
	if request.method == 'POST':
		req = request.get_json()

		filtering = {
			"GCRecord": None,
			"DevUniqueId": req["DevUniqueId"]
		}

		thisDevice = Device.query.filter_by(**filtering).first()

		data = {}
		if thisDevice:
			data = thisDevice.to_json_api()

		else:
			database = Db_inf.query.first()
			req["DbInfGuid"] = str(database.DbInfGuid) if database else None

			r = requests.post(
				f"{Config.SAP_SERVICE_URL}{Config.SAP_SERVICE_URL_PREFIX}/devices/register/",
				data = json.dumps(req),
				headers = {
					'Content-Type': 'application/json',
					'x-access-token': Config.SAP_SERVICE_KEY})

			try:
				server_response = r.json()

			except Exception as ex:
				print(f"{datetime.now()} | Device register response json Exception: {ex}")

			if (r.status_code == 200 or r.status_code == 201):
				if server_response["status"] != 0:
					data = addDeviceDict(server_response["data"])
					data["RpAccId"] = None

					try:
						thisDevice = Device(**data)
						db.session.add(thisDevice)
						db.session.commit()

					except Exception as ex:
						print(f"{datetime.now()} | Device register db insertion Exception: {ex}")

		res = {
			"status": 1 if data else 0,
			"data": data,
			"message": "Device registration",
			"total": 1 if data else 0
		}
		response = make_response(jsonify(res), 200)

		return response