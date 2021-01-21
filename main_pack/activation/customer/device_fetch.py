from flask import jsonify, request, make_response, abort
import json
import requests
from datetime import datetime

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.api.auth.utils import token_required
from main_pack.api.users.utils import addDeviceDict

from main_pack.models.users.models import Device
from main_pack.models.base.models import Db_inf


@api.route("/devices/fetch/",methods=["GET"])
@token_required
def fetch_device(user):
	model_type = user["model_type"]
	current_user = user["current_user"]

	if model_type == "rp_acc":
		abort(401)

	if not current_user.is_admin():
		abort(401)

	database = Db_inf.query.first()
	db_guid = database.DbInfGuid

	r = requests.get(
		f"{Config.SAP_SERVICE_URL}/devices/fetch/?uuid={db_guid}",
		headers = {
			'Content-Type': 'application/json',
			'x-access-token': Config.SAP_SERVICE_KEY,
			}
		)

	try:
		server_response = r.json()
	except Exception as ex:
		print(f"{datetime.now()} | Service response json Exception: {ex}")

	data = {}

	if (r.status_code == 200 or r.status_code == 201):
		if server_response["status"] == 0:
			abort(400)

		server_data = server_response["data"]
		service_devices = server_data["Devices"]

		customer_devices = Device.query.filter_by(GCRecord = None).all()
		untracked_devices = []

		for device in customer_devices:
			current_server_device = [dev for dev in service_devices if dev["DevUniqueId"] == device.DevUniqueId]

			if current_server_device:
				current_server_device = current_server_device[0]
				device_info = addDeviceDict(current_server_device)
				device.update(**device_info)
				service_devices.pop(service_devices.index(current_server_device))

			else:
				device.IsAllowed = False
				untracked_devices.append(device.to_json_api())
				# # !!! TODO: sycnhronise untracked with main server
				# r = requests.post(
				# 	f"{Config.SAP_SERVICE_URL}/devices/synch/",
				# 	data = json.dumps({"Devices": untracked_devices}),
				# 	headers = {
				# 		'Content-Type': 'application/json',
				# 		'x-access-token': Config.SAP_SERVICE_KEY}
				# 	)


		if service_devices:
			for device in service_devices:
				device_info = addDeviceDict(device)
				thisDevice = Device(**device_info)
				db.session.add(thisDevice)					

		db.session.commit()

		updated_customer_devices = Device.query.filter_by(GCRecord = None).all()
		data = {
			"DeviceQty": server_data["DeviceQty"],
			"UnusedDeviceQty": server_data["UnusedDeviceQty"],
			"Devices": [device.to_json_api() for device in updated_customer_devices]
		}

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Device registration",
		"total": 1 if data else 0
	}
	response = make_response(jsonify(res), 200)

	return response