from flask import jsonify, request, make_response, abort
from datetime import datetime
from sqlalchemy.orm import joinedload

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.models.users.models import Device, Rp_acc
from main_pack.models.base.models import Db_inf

from .utils import sap_key_required


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

		allowed_devices = [device for device in rp_acc.Device if rp_acc.Device.IsAllowed not rp_acc.Device.GCRecord]
		print("server code!!!")
		print(allowed_devices)

		# !!! TODO: Add validation time and key update

		while (len(allowed_devices) > allowed_device_qty):
			forbidding_device = allowed_devices.pop()
			print('forbidding_device')
			print(forbidding_device.DevUniqueId)
			forbidding_device.IsAllowed = False

		db.session.commit()

		print("prining devicesss")
		devices = [device.to_json_api() for device in rp_acc.Device if not rp_acc.Device.GCRecord]
		print(devices)
		dev = Device.query.filter_by(GCRecord = None).all()
		devs = [dev.to_json_api() for dev in devs]
		print(devs)
		unused_device_qty = allowed_device_qty - len(allowed_devices)

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