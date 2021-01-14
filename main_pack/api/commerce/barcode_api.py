# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.commerce.models import Barcode
from main_pack.api.commerce.utils import addBarcodeDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-barcodes/",methods=['GET','POST'])
@sha_required
def api_barcodes():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		barcodes = Barcode.query.filter_by(GCRecord = None)
		if DivId:
			barcodes = barcodes.filter_by(DivId = DivId)
		if notDivId:
			barcodes = barcodes.filter(Barcode.DivId != notDivId)
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			barcodes = barcodes.filter(Barcode.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		barcodes = barcodes.all()
		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "All barcodes",
			"data": [barcode.to_json_api() for barcode in barcodes],
			"total": len(barcodes)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			barcodes = []
			failed_barcodes = [] 
			for barcode_req in req:
				barcode = addBarcodeDict(barcode_req)
				try:
					ResId = barcode['ResId']
					UnitId = barcode['UnitId']
					thisBarcode = Barcode.query\
						.filter_by(ResId = ResId, UnitId = UnitId)\
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
			response = make_response(jsonify(res),201)
	return response