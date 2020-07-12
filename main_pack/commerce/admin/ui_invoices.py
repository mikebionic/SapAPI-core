from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.models.commerce.models import (Inv_line,Inv_line_det,Inv_line_det_type,
	Inv_status,Inv_type,Invoice,Order_inv,Order_inv_line,Order_inv_type)
from sqlalchemy import and_
from main_pack.base.num2text import num2text,price2text
import decimal
from flask import current_app
# invoiceRegNo
# orderInvRegNo
# >> search in db for presets
# inv_statusId
# put the models inv stat is the new id

@bp.route('/ui/inv_status/',methods=['POST'])
def ui_inv_status():
	req = request.get_json()
	InvRegNo = req.get("invRegNo")
	OInvRegNo = req.get('oInvRegNo')
	InvStatId = req.get('invStatId')
	try:
		if InvRegNo:
			invModel = Invoice.query\
				.filter(and_(Invoice.GCRecord=='' or Invoice.GCRecord==None),\
					Invoice.InvRegNo==InvRegNo).first()
		elif OInvRegNo:
			invModel = Order_inv.query\
				.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
					Order_inv.OInvRegNo==OInvRegNo).first()

		invModel.InvStatId = InvStatId
		db.session.commit()
		response = jsonify({
			'status':'updated',
			'responseText':gettext('Invoice status')+' '+gettext('successfully updated'),
		})
	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})
	return response


@bp.route('/ui/order_inv/',methods=['POST','DELETE'])
def ui_order_inv():
	try:
		if request.method == 'POST':

			# {
			# 	"oInvRegNo": "ARSSFK8119,"
			# 	"oInvTotalPrice":134.22
			# 	"products": [
			# 		"productId":23,
			# 		"productPrice": 10,
			# 		"productQty": 1,
			# 		"totalPrice": 10,
			# 	]
			# }

			req = request.get_json()
			OInvRegNo = req.get('oInvRegNo')
			OInvTotal = req.get('oInvTotalPrice')
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(OInvFTotal,
						current_app.config['PRICE_2_TEXT_LANGUAGE'],
						current_app.config['PRICE_2_TEXT_CURRENCY'])
			thisOInv = Order_inv.query\
				.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
					Order_inv.OInvRegNo==OInvRegNo).first()
			products = req.get('products')
			for product in products:
				try:
					thisOInvLine = Order_inv_line.query\
						.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
							Order_inv_line.OInvLineId==product['productId']).first()
					if (thisOInv.OInvId == thisOInvLine.OInvId):
						thisOInvLine.OInvLinePrice = decimal.Decimal(product['productPrice'])
						thisOInvLine.OInvLineAmount = product['productQty']
						thisOInvLine.OInvLineTotal = decimal.Decimal(product['totalPrice'])
						thisOInvLine.OInvLineFTotal = decimal.Decimal(product['totalPrice'])
					thisOInv.OInvTotal = decimal.Decimal(OInvTotal)
					thisOInv.OInvFTotal = decimal.Decimal(OInvFTotal)
					thisOInv.OInvFTotalInWrite = OInvFTotalInWrite
					db.session.commit()
					response = jsonify({
						'status':'updated',
						'responseText':gettext('successfully updated'),
						})
				except:
					response = jsonify({
						'status':'error',
						'responseText':gettext('Unknown error!'),
						})

		elif request.method == 'DELETE':
			req = request.get_json()
			OInvLineId = req.get('productId')
			OInvRegNo = req.get('oInvRegNo')
			
			# checking if line exists
			thisOInvLine = Order_inv_line.query\
			.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
				Order_inv_line.OInvLineId==OInvLineId).first()
			# checking if order inv exists
			thisOInv = Order_inv.query\
				.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
					Order_inv.OInvRegNo==OInvRegNo).first()
			# check if the line is the correct orders line
			if (thisOInv.OInvId == thisOInvLine.OInvId):
				thisOInvLine.GCRecord = 1
				db.session.commit()
				
				response = jsonify({
					'status':'deleted',
					'responseText':gettext('successfully deleted'),
					})
			else:
				raise(Exception)
	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})
	return response