from flask import jsonify, request, make_response, abort
from datetime import datetime
import uuid

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.api.users.utils import addDeviceDict
from main_pack.api.base.validators import request_is_json
from main_pack.models import Device, Rp_acc
from .utils import sap_key_required
from main_pack.base.cryptographyMethods import encrypt_data


@api.route("/devices/register/",methods=["POST"])
@sap_key_required
@request_is_json(request)
def register_device():
	req = request.get_json()
	rp_acc = Rp_acc.query.filter_by(DbGuid = req["DbInfGuid"], GCRecord = None).first()

	if not rp_acc:
		abort(400)

	RpAccId = rp_acc.RpAccId

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

			# DevVerifyDate = datetime.now().replace(microsecond = 0)
			# device_info["DevVerifyDate"] = DevVerifyDate

			# verify_date_data = str(DevVerifyDate.timestamp())

			# DevVerifyKey = encrypt_data(
			# 	data = verify_date_data,
			# 	server_key = Config.BASE_32_FERNET_KEY.encode(),
			# 	db_guid = rp_acc.DbGuid,
			# 	client_key = rp_acc.RpAccWebKey
			# )

			# if not DevVerifyKey:
			# 	raise Exception

			# device_info["DevVerifyKey"] = DevVerifyKey

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