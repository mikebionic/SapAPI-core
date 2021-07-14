# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.auth.utils import sha_required

from main_pack.api.v1.barcode_api import api
from main_pack.api.v1.barcode_api.utils import collect_barcode_data


@api.route("/tbl-barcodes/", methods=['GET'])
@sha_required
def tbl_barcode_get():
	arg_data = {
		"BarcodeId": request.args.get("id",None,type=int),
		"BarcodeGuid": request.args.get("barcodeGuid","",type=str),
		"CId": request.args.get("companyId",None,type=int),
		"DivId": request.args.get("DivId",None,type=int),
		"ResId": request.args.get("resourceId",None,type=int),
		"UnitId": request.args.get("unitId",None,type=int),
		"BarcodeVal": request.args.get("barcodeVal","",type=str),
	}

	data = collect_barcode_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Media",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)