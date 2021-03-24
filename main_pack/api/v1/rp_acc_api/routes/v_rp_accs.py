# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.rp_acc_api import api
from main_pack.api.auth.utils import token_required
from main_pack.api.v1.rp_acc_api.utils import collect_rp_acc_data


@api.route("/v-rp-accs/")
@token_required
def v_rp_accs():
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"DivGuid": request.args.get("DivGuid",None,type=str),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"RpAccId": request.args.get("id",None,type=int),
		"RpAccRegNo": request.args.get("regNo","",type=str),
		"RpAccName": request.args.get("name","",type=str),
		"UId": request.args.get("userId",None,type=int),
		"EmpId": request.args.get("empId",None,type=int)
	}

	arg_data["withPassword"] = 1
	data = collect_rp_acc_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Rp_acc",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response