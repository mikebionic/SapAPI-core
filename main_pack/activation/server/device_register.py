from flask import jsonify, request, make_response, abort
from datetime import datetime
import uuid

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.api.users.utils import addDeviceDict
from main_pack.api.base.validators import request_is_json
from main_pack.models.users.models import Device, Rp_acc
from .utils import sap_key_required


@api.route("/devices/register/",methods=["POST"])
@sap_key_required
@request_is_json
def register_device():
	if request.method == 'POST':
		req = request.get_json()

		rp_acc = Rp_acc.query.filter_by(DbGuid = "DbInfGuid", GCRecord = None).first()
		RpAccId = rp_acc.RpAccId if rp_acc else None

		filtering = {
			"GCRecord": None,
			"DevUniqueId": req["DevUniqueId"],
			"RpAccId": RpAccId
		}

		thisDevice = Device.query.filter_by(**filtering).first()

		data = {}
		if thisDevice:
			data = thisDevice.to_json_api()

		else:
			try:
				device_info = addDeviceDict(req)
				device_info["RpAccId"] = RpAccId
				device_info["DevGuid"] = uuid.uuid4()
				thisDevice = Device(**device_info)
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

		response = make_response(jsonify(res), 200)

		return response