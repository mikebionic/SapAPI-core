# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack.api.auth.utils import token_required
from main_pack.api.v1.warehouse_api import api
from main_pack.api.v1.warehouse_api.utils import collect_warehouse_data


@api.route("/v-warehouses/")
@token_required
def v_warehouse(user):
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"WhId": request.args.get("id",None,type=int),
		"WhName": request.args.get("name","",type=str)
	}

	data = collect_warehouse_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Warehouses",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)