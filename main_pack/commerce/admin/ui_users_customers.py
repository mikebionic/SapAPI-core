from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.models.users.models import Users,Rp_acc
from sqlalchemy import and_

@bp.route('/ui/customers_table/', methods=['POST','DELETE'])
@login_required
@ui_admin_required
def ui_customers_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			RpAccId = req.get('rpAccId')
			RpAccTypeId = req.get('rpAccTypeId')
			RpAccStatusId = req.get('rpAccStatusId')
			rp_acc = Rp_acc.query\
				.filter_by(GCRecord = None, RpAccId = RpAccId)\
				.first()
			if rp_acc:
				if RpAccTypeId:
					rp_acc.RpAccTypeId = RpAccTypeId
					db.session.commit()
				if RpAccStatusId:
					rp_acc.RpAccStatusId = RpAccStatusId
					db.session.commit()
				response = jsonify({
					"status": "updated",
					"responseText": rp_acc.RpAccName+' '+gettext('successfully updated'),
					})
		elif request.method == 'DELETE':
			req = request.get_json()
			RpAccId = req.get('rpAccId')
			thisRpAcc = Rp_acc.query\
				.filter_by(GCRecord = None, RpAccId = RpAccId)\
				.first()

			# handling the deletion if invoice exists
			errors = []
			invoices = [invoice.to_json_api() for invoice in thisRpAcc.Invoice if invoice.GCRecord == None]
			inv_lines = [inv_line.to_json_api() for inv_line in thisRpAcc.Inv_line if inv_line.GCRecord == None]
			order_invoices = [order_inv.to_json_api() for order_inv in thisRpAcc.Order_inv if order_inv.GCRecord == None]
			order_inv_lines = [order_inv_line.to_json_api() for order_inv_line in thisRpAcc.Order_inv_line if order_inv_line.GCRecord == None]
			
			if invoices:
				errors.append({"message": "Invoices", "data": invoices})
			if inv_lines:
				errors.append({"message": "Invoice lines", "data": inv_lines})
			if order_invoices:
				errors.append({"message": "Order invoices", "data": order_invoices})
			if order_inv_lines:
				errors.append({"message": "Order invoice lines", "data": order_inv_lines})
			
			if errors:
				issues_text = ''
				for error in errors:
					issues_text += ' {} '.format(error["message"])
				response = jsonify({
					"status": "error",
					"responseText": gettext('Failed')+'! [{}]'.format(issues_text),
					"errors": errors
					})
				return response

			thisRpAcc.GCRecord = 1
			user = Users.query\
				.filter_by(GCRecord = None, RpAccId = RpAccId)\
				.first()
			if user:
				user.GCRecord=1

			db.session.commit()
			response = jsonify({
				"status": "deleted",
				"responseText": thisRpAcc.RpAccName+' '+gettext('successfully deleted'),
				})
	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": "error",
			"responseText": gettext('Unknown error!'),
			})
	return response

@bp.route('/ui/users_table/', methods=['POST','DELETE'])
@login_required
@ui_admin_required
def ui_users_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			UId = req.get('userId')
			UTypeId = req.get('userTypeId')
			user = Users.query\
				.filter_by(GCRecord = None, UId = UId)\
				.first()
			if user:
				if UTypeId:
					user.UTypeId = UTypeId
					db.session.commit()
				response = jsonify({
					"status": "updated",
					"responseText": user.UName+' '+gettext('successfully updated'),
					})
		elif request.method == 'DELETE':
			req = request.get_json()
			UId = req.get('userId')
			thisUser = Users.query.get(UId)

			# handling the deletion if invoice exists
			errors = []
			rp_accs = [rp_acc.to_json_api() for rp_acc in thisRpAcc.Rp_acc if rp_acc.GCRecord == None]
			
			if rp_accs:
				errors.append({"message": "Customers", "data": rp_accs})
			
			if errors:
				issues_text = ''
				for error in errors:
					issues_text += ' {} '.format(error["message"])
				response = jsonify({
					"status": "error",
					"responseText": gettext('Failed')+'! [{}]'.format(issues_text),
					"errors": errors
					})
				return response


			thisUser.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": "deleted",
				"responseText": thisUser.UName+' '+gettext('successfully deleted'),
				})
	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": "error",
			"responseText": gettext('Unknown error!'),
			})
	return response