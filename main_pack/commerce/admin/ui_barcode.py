from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import addBarcodeDict
from main_pack.models.commerce.models import Barcode


@bp.route('/ui/barcode/', methods=['GET','POST','PUT'])
def ui_barcode():
	if request.method == 'POST':
		req = request.get_json()
		barcode = addBarcodeDict(req)
		print(barcode)
		barcodeId = req.get('barcodeId')
		if (barcodeId == '' or barcodeId == None):
			newBarcode = Barcode(**barcode)
			db.session.add(newBarcode)
			print(newBarcode)
			db.session.commit()
			response = jsonify({
				'barcodeId':newBarcode.BarcodeId,
				'status':'created',
				'responseText':gettext('Barcode')+' '+gettext('successfully saved'),
				'htmlData': render_template('/commerce/admin/barcodeAppend.html',barcode=newBarcode)
				})
			print(response)
		else:
			try:
				updateBarcode = Barcode.query.get(int(barcodeId))
				updateBarcode.update(**barcode)
				updateBarcode.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
						'barcodeId':updateBarcode.BarcodeId,
						'status':'updated',
						'responseText':gettext('Barcode')+' '+gettext('successfully updated'),
						'htmlData': render_template('/commerce/admin/barcodeAppend.html',barcode=updateBarcode)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	if request.method == 'DELETE':
		req = request.get_json()
		barcodeId = req.get('barcodeId')
		thisBarcode = Barcode.query.get(barcodeId)
		thisBarcode.GCRecord == 1
		response = jsonify({
			'barcodeId':thisBarcode.BarcodeId,
			'status':'deleted',
			'responseText':gettext('Barcode')+' '+gettext('successfully deleted')
		})
	return response