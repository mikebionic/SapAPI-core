# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime, timedelta
import dateutil.parser

from . import api
from main_pack import db

from .utils import addBarcodeDict
from main_pack.models import Barcode
from main_pack.api.base.validators import request_is_json
from main_pack.api.auth.utils import admin_required
from main_pack.base.apiMethods import checkApiResponseStatus


@api.route("/tbl-dk-barcodes/",methods=['GET','POST'])
@admin_required
@request_is_json(request)
def api_barcodes(user):
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		BarcodeId = request.args.get("id",None,type=int)
		BarcodeVal = request.args.get("val","",type=str)

		filtering = {"GCRecord": None}

		if DivId:
			filtering["DivId"] = DivId
		if BarcodeId:
			filtering["BarcodeId"] = BarcodeId
		if BarcodeVal:
			filtering["BarcodeVal"] = BarcodeVal

		barcodes = Barcode.query.filter_by(**filtering)

		if notDivId:
			barcodes = barcodes.filter(Barcode.DivId != notDivId)

		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			barcodes = barcodes.filter(Barcode.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

		data = [barcode.to_json_api() for barcode in barcodes.all()]

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Barcodes",
			"data": data,
			"total": len(data)
		}

		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = [] 

		for barcode_req in req:
			barcode = addBarcodeDict(barcode_req)
			try:
				filtering = {"GCRecord": None}
				filtering["ResId"] = barcode['ResId']
				filtering["UnitId"] = barcode['UnitId']
				thisBarcode = Barcode.query\
					.filter_by(**filtering)\
					.first()

				if thisBarcode:
					thisBarcode.update(**barcode)
					data.append(barcode)

				else:
					newBarcode = Barcode(**barcode)
					db.session.add(newBarcode)
					data.append(barcode)

			except Exception as ex:
				print(f"{datetime.now()} | Barcode Api Exception: {ex}")
				failed_data.append(barcode)

		db.session.commit()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response