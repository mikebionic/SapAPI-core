from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db_test,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce_test.admin import bp

from main_pack.models_test.commerce.models import (Inv_line,
																							Inv_line_det,
																							Inv_line_det_type,
																							Inv_status,
																							Inv_type,
																							Invoice,
																							Order_inv,
																							Order_inv_line,
																							Order_inv_type)
from sqlalchemy import and_
from main_pack.base.num2text import num2text, price2text
import decimal
from main_pack.config import Config
from main_pack.models_test.commerce.models import Res_total
from main_pack.base.invoiceMethods import totalQtySubstitution

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
		db_test.session.commit()
		response = jsonify({
			"status": 'updated',
			"responseText": gettext('Invoice status')+' '+gettext('successfully updated'),
		})
	except Exception as ex:
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
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
						Config.PRICE_2_TEXT_LANGUAGE,
						Config.PRICE_2_TEXT_CURRENCY)
			thisOInv = Order_inv.query\
				.filter(and_(
					Order_inv.GCRecord == '' or Order_inv.GCRecord == None),\
					Order_inv.OInvRegNo == OInvRegNo).first()
			products = req.get('products')
			for product in products:
				try:
					# check for presence and equality with the editing product
					thisOInvLine = Order_inv_line.query\
						.filter(and_(
							Order_inv_line.GCRecord == '' or Order_inv_line.GCRecord == None),\
							Order_inv_line.OInvLineId == product['productId']).first()
					# check the connection of OInvLine to the correct OInv
					if (thisOInv.OInvId == thisOInvLine.OInvId):
						OInvLineAmount = product['productQty']
						OInvLinePrice = decimal.Decimal(product['productPrice'])
						OInvLineTotal = decimal.Decimal(product['totalPrice'])

						## !!! check if new quantity is greater or not
						# check if the quantity value is positive else exception
						# if greater - substitude upcoming with present (get the qty of increased)
						# decrement the resId with result (if config allows the negative values)
						# if smaller - substitude present with upcoming
						# increment the resId with result
						##

						if (OInvLineAmount <= 0):
							OInvLineAmount = 1
							# # uncomment if I don't want to equal to 1 for errors
							# print("amount is less than 1: ")
							# raise Exception
						res_total = Res_total.query\
							.filter(and_(
								Res_total.GCRecord == '' or Res_total.GCRecord == None),\
								Res_total.ResId == thisOInvLine.ResId).first()

						print(res_total.ResTotBalance)
						pastQty = thisOInvLine.OInvLineAmount
						if (pastQty<OInvLineAmount):
							resulting_changes = OInvLineAmount-pastQty
							print("substituded greater with result"+str(resulting_changes))
							totalSubstitutionResult = totalQtySubstitution(res_total.ResTotBalance,resulting_changes)
							
							if totalSubstitutionResult['status'] == 0:
								raise Exception

							res_total.ResTotBalance = totalSubstitutionResult['totalBalance']
						elif (pastQty>OInvLineAmount):
							resulting_changes = pastQty - OInvLineAmount
							res_total.ResTotBalance += resulting_changes

						thisOInvLine.OInvLinePrice = OInvLinePrice
						thisOInvLine.OInvLineAmount = OInvLineAmount
						thisOInvLine.OInvLineTotal = OInvLineTotal
						thisOInvLine.OInvLineFTotal = OInvLineTotal

					thisOInv.OInvTotal = decimal.Decimal(OInvTotal)
					thisOInv.OInvFTotal = decimal.Decimal(OInvFTotal)
					thisOInv.OInvFTotalInWrite = OInvFTotalInWrite
					db_test.session.commit()
					response = jsonify({
						"status": 'updated',
						"responseText": gettext('successfully updated'),
						})
				except Exception as ex:
					response = jsonify({
						"status": 'error',
						"responseText": gettext('Unknown error!'),
						})

		elif request.method == 'DELETE':
			req = request.get_json()
			OInvLineId = req.get('productId')
			OInvRegNo = req.get('oInvRegNo')
			
			# checking if line exists
			thisOInvLine = Order_inv_line.query\
			.filter(and_(
				Order_inv_line.GCRecord == '' or Order_inv_line.GCRecord == None),\
				Order_inv_line.OInvLineId == OInvLineId).first()
			# checking if order inv exists
			thisOInv = Order_inv.query\
				.filter(and_(
					Order_inv.GCRecord == '' or Order_inv.GCRecord == None),\
					Order_inv.OInvRegNo == OInvRegNo).first()
			# check if the line is the correct orders line
			if (thisOInv.OInvId == thisOInvLine.OInvId):
				thisOInvLine.GCRecord = 1
				db_test.session.commit()
				
				response = jsonify({
					"status": 'deleted',
					"responseText": gettext('successfully deleted'),
					})
			else:
				raise(Exception)
	except Exception as ex:
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})
	return response