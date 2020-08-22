from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from main_pack.config import Config

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import addBarcodeDict
from main_pack.models.commerce.models import Barcode


@bp.route('/ui/barcode/', methods=['POST','DELETE'])
@login_required
@ui_admin_required()
def ui_barcode():
	if request.method == 'POST':
		req = request.get_json()
		barcode = addBarcodeDict(req)
		barcodeId = req.get('barcodeId')
		if (barcodeId == '' or barcodeId == None):
			newBarcode = Barcode(**barcode)
			db.session.add(newBarcode)
			db.session.commit()
			response = jsonify({
				"barcodeId": newBarcode.BarcodeId,
				"status": "created",
				"responseText": gettext('Barcode')+' '+gettext('successfully saved'),
				"htmlData":  render_template(Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH+"barcodeAppend.html",barcode=newBarcode)
				})
		else:
			try:
				updateBarcode = Barcode.query.get(int(barcodeId))
				updateBarcode.update(**barcode)
				updateBarcode.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
						"barcodeId": updateBarcode.BarcodeId,
						"status": "updated",
						"responseText": gettext('Barcode')+' '+gettext('successfully updated'),
						"htmlData":  render_template(Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH+"barcodeAppend.html",barcode=updateBarcode)
					})
			except Exception as ex:
				print(ex)
				response = jsonify({
					"status": "error",
					"responseText": gettext('Unknown error!'),
					})
	if request.method == 'DELETE':
		req = request.get_json()
		barcodeId = req.get('barcodeId')
		thisBarcode = Barcode.query.get(barcodeId)
		thisBarcode.GCRecord == 1
		response = jsonify({
			"barcodeId": thisBarcode.BarcodeId,
			"status": "deleted",
			"responseText": gettext('Barcode')+' '+gettext('successfully deleted')
		})
	return response