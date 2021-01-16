# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.commerce.models import Barcode
from main_pack.api.commerce.utils import addBarcodeDict
from main_pack import db
from flask import current_app
from main_pack.api.base.validators import request_is_json
from main_pack.api.auth.utils import sha_required


@api.route("/tbl-dk-barcodes/",methods=['GET','POST'])
@sha_required
@request_is_json
def api_barcodes():
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

		barcodes = []
		failed_barcodes = [] 

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
					barcodes.append(barcode)
				else:
					newBarcode = Barcode(**barcode)
					db.session.add(newBarcode)
					barcodes.append(barcode)

			except Exception as ex:
				print(f"{datetime.now()} | Barcode Api Exception: {ex}")
				failed_barcodes.append(barcode)

		db.session.commit()
		status = checkApiResponseStatus(barcodes,failed_barcodes)

		res = {
			"data": barcodes,
			"fails": failed_barcodes,
			"success_total": len(barcodes),
			"fail_total": len(failed_barcodes)
		}
		for e in status:
			res[e] = status[e]
		# !!! TODO: Make a proper response code validation
		response = make_response(jsonify(res), 201)
	return response