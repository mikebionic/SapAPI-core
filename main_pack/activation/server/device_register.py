from flask import jsonify, request, make_response, abort
from datetime import datetime
import uuid

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.api.base.validators import request_is_json
from main_pack.models.users.models import Device
from .utils import sap_key_required


@api.route("/devices/register/",methods=["POST"])
@sap_key_required
@request_is_json
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
			try:
				req["DevGuid"] = uuid.uuid4()
				thisDevice = Device(**req)
				db.session.add(thisDevice)
				db.session.commit()

				data = thisDevice.to_json_api()

			except Exception as ex:
				print(f"{datetime.now()} | Device register server Exception: {ex}")

		res = {
			"status": 1 if data else 0,
			"data": data,
			"message": "Device registration",
			"total": 1 if data else 0
		}

		response = make_response(jsonify(res),200)

		return response