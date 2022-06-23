# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import admin_required

from main_pack.api.v1.user_api import api
from main_pack.api.v1.user_api.utils import collect_user_data


@api.route("/tbl-users/")
@admin_required
def tbl_user_get(user):
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"UId": request.args.get("id",None,type=int),
		"URegNo": request.args.get("regNo","",type=str),
		"UName": request.args.get("name","",type=str),
		"withImage": request.args.get("withImage",0,type=int),
	}

	arg_data["withPassword"] = 1
	data = collect_user_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "User",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)