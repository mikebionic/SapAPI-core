# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.config import Config
from main_pack.api.v1.device_api import api
from main_pack.api.v1.device_api.utils import save_device_sync_data
from main_pack.activation.customer.device_fetch import fetch_device


@api.route("/tbl-devices/", methods=['POST'])
@admin_required
@request_is_json(request)
def tbl_device_post(user):
	req = request.get_json()
	data = []
	device_data, fails = save_device_sync_data(req)
	succeded_devices = [device_info["DevUniqueId"] for device_info in data if "DevUniqueId" in device_info]

	if Config.USE_SERVERLESS_ACTIVATION:
		data = device_data

	else:
		fetch_response = fetch_device()
		if succeded_devices and fetch_response:
			for device in fetch_response["data"]["Devices"]:
				try:
					if "DevUniqueId" in device:
						succeded_devices[succeded_devices.index(device["DevUniqueId"])]
						data.append(device)
				except:
					pass

	status = checkApiResponseStatus(data, fails)
	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)