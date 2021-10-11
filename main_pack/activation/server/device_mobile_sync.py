from flask import jsonify, request, make_response, abort
import uuid

from . import api
from main_pack import db
from main_pack.api.users.utils import addDeviceDict
from main_pack.api.base.validators import request_is_json
from main_pack.models import Device, Rp_acc
from main_pack.base import log_print

@api.route("/devices/mobile-sync/",methods=["POST"])
@request_is_json(request)
def device_mobile_sync():
	req = request.get_json()
	data, message = process_mobile_sync_data(req)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": message if message else "Device mobile sync",
		"total": 1 if data else 0
	}

	response = make_response(jsonify(res), 200)
	return response


def process_mobile_sync_data(req):
	data, message = [], ""
	try:
		if "Devices" not in req:
			raise Exception

		DbGuid = req["DbInfGuid"]
		rp_acc_model = Rp_acc.query.filter_by(DbGuid = DbGuid, GCRecord = None).first()
		if not rp_acc_model:
			abort(400)

		RpAccId = rp_acc_model.RpAccId
		for device_req in req["Devices"]:
			filtering = {
				"GCRecord": None,
				"DevUniqueId": device_req["DevUniqueId"],
				"RpAccId": RpAccId
			}

			thisDevice = Device.query.filter_by(**filtering).first()
			if not thisDevice:
				device_info = addDeviceDict(device_req)
				device_info["RpAccId"] = RpAccId
				if not device_info["DevGuid"]:
					device_info["DevGuid"] = uuid.uuid4()

				thisDevice = Device(**device_info)
				db.session.add(thisDevice)
				db.session.commit()

			devices_filtering = {
				"GCRecord": None,
				"RpAccId": RpAccId
			}
			rp_devices = Device.query.filter_by(**devices_filtering).all()

			allowed_device_qty = rp_acc_model.DeviceQty
			unused_device_qty = rp_acc_model.UnusedDeviceQty
			allowed_devices = [rp_device for rp_device in rp_devices if rp_device.IsAllowed]

			while (len(allowed_devices) > allowed_device_qty):
				forbidding_device = allowed_devices.pop()
				forbidding_device.IsAllowed = False

			unused_device_qty = allowed_device_qty - len(allowed_devices)
			if rp_acc_model.UnusedDeviceQty != unused_device_qty:
				rp_acc_model.UnusedDeviceQty = unused_device_qty

			db.session.commit()
			devices_list = [rp_device.to_json_api() for rp_device in rp_devices]

			data = {
				"DbGuid": DbGuid,
				"DeviceQty": allowed_device_qty,
				"UnusedDeviceQty": unused_device_qty,
				"Devices": devices_list
			}

	except Exception as ex:
		log_print(f"Device mobile sync server Exception: {ex}")

	return data, message