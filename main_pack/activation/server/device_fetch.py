from flask import jsonify, request, make_response, abort
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.models.users.models import Device, Rp_acc
from main_pack.models.base.models import Db_inf

from .utils import sap_key_required
from main_pack.base.cryptographyMethods import encrypt_data


@api.route("/devices/fetch/",methods=["GET"])
@sap_key_required
def fetch_device():
	db_guid = request.args.get("uuid",None,type=str)

	rp_acc = Rp_acc.query\
		.filter_by(GCRecord = None, DbGuid = db_guid)\
		.options(joinedload(Rp_acc.Device))\
		.first()

	data = {}

	if rp_acc:
		allowed_device_qty = rp_acc.DeviceQty
		unused_device_qty = rp_acc.UnusedDeviceQty

		allowed_devices = [device for device in rp_acc.Device if device.IsAllowed and not device.GCRecord]

		while (len(allowed_devices) > allowed_device_qty):
			forbidding_device = allowed_devices.pop()
			forbidding_device.IsAllowed = False

		unused_device_qty = allowed_device_qty - len(allowed_devices)

		for device in rp_acc.Device:
			if not device.GCRecord:
				DevVerifyDate = datetime.now()
				device.DevVerifyDate = DevVerifyDate

				verify_date_data = str(DevVerifyDate.replace(tzinfo=timezone.utc).timestamp())

				updated_key = encrypt_data(
					data = verify_date_data,
					server_key = Config.BASE_32_FERNET_KEY.encode(),
					db_guid = rp_acc.DbGuid,
					client_key = rp_acc.RpAccWebKey
				)
				device.DevVerifyKey = updated_key

		db.session.commit()

		devices = [device.to_json_api() for device in rp_acc.Device if not device.GCRecord]

		if rp_acc.UnusedDeviceQty != unused_device_qty:
			rp_acc.UnusedDeviceQty = unused_device_qty
			db.session.commit()

		data = {
			"DbGuid": db_guid,
			"DeviceQty": allowed_device_qty,
			"UnusedDeviceQty": unused_device_qty,
			"Devices": devices
		}

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Device fetch",
		"total": 1 if data else 0
	}

	response = make_response(jsonify(res), 200)

	return response