from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Barcode
from main_pack.api.commerce.utils import addBarcodeDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required

@api.route("/tbl-dk-barcodes/",methods=['GET','POST','PUT'])
@sha_required
def api_barcodes():
	if request.method == 'GET':
		barcodes = Barcode.query.filter_by(GCRecord = None).all()
		res = {
			"status": 1,
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
			for barcode in req:
				barcode = addBarcodeDict(barcode)
				try:
					if not 'BarcodeId' in barcode:
						newBarcode = Barcode(**barcode)
						db.session.add(newBarcode)
						db.session.commit()
						barcodes.append(barcode)
					else:
						BarcodeId = barcode['BarcodeId']
						thisBarcode = Barcode.query.get(int(BarcodeId))
						if thisBarcode is not None:
							# check for presenting in database
							thisBarcode.update(**barcode)
							# thisBarcode.modifiedInfo(UId=1)
							db.session.commit()
							barcodes.append(barcode)

						else:
							# create new barcode
							newBarcode = Barcode(**barcode)
							db.session.add(newBarcode)
							db.session.commit()
							barcodes.append(barcode)
				except Exception as ex:
					print(ex)
					failed_barcodes.append(barcode)

			status = checkApiResponseStatus(barcodes,failed_barcodes)
			res = {
				"data": barcodes,
				"fails": failed_barcodes,
				"success_total": len(barcodes),
				"fail_total": len(failed_barcodes)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),201)
	return response