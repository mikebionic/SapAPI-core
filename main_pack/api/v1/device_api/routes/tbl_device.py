# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import admin_required

from main_pack.api.v1.device_api import api
from main_pack.api.v1.device_api.utils import collect_device_data


@api.route("/tbl-devices/")
@admin_required
def tbl_device_get(user):
	arg_data = {
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"DevId": request.args.get("id",None,type=int),
		"RpAccId": request.args.get("rpaccId",None,type=int),
		"UId": request.args.get("userId",None,type=int),
		"IsAllowed": request.args.get("isAllowed",None,type=int),
		"DevUniqueId": request.args.get("uniqueId","",type=str),
		"DevName": request.args.get("name","",type=str),
	}

	data = collect_device_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Device",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)