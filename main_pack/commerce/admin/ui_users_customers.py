from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.models.users.models import Users,Rp_acc
from sqlalchemy import and_

@bp.route('/ui/customers_table/', methods=['POST','DELETE'])
def ui_customers_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			RpAccId = req.get('rpAccId')
			RpAccTypeId = req.get('rpAccTypeId')
			RpAccStatusId = req.get('rpAccStatusId')
			rp_acc = Rp_acc.query\
				.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
					Rp_acc.RpAccId==RpAccId).first()
			if rp_acc:
				if RpAccTypeId:
					rp_acc.RpAccTypeId = RpAccTypeId
					db.session.commit()
				if RpAccStatusId:
					rp_acc.RpAccStatusId = RpAccStatusId
					db.session.commit()
				response = jsonify({
					"status": 'updated',
					"responseText": rp_acc.RpAccName+' '+gettext('successfully updated'),
					})
		elif request.method == 'DELETE':
			req = request.get_json()
			RpAccId = req.get('rpAccId')
			thisRpAcc = Rp_acc.query.get(RpAccId)
			thisRpAcc.GCRecord = 1

			user = Users.query\
				.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
					Users.RpAccId==RpAccId).first()
			if user:
				user.GCRecord=1

			db.session.commit()
			response = jsonify({
				"status": 'deleted',
				"responseText": thisRpAcc.RpAccName+' '+gettext('successfully deleted'),
				})
	except Exception as ex:
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})
	return response

@bp.route('/ui/users_table/', methods=['POST','DELETE'])
def ui_users_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			UId = req.get('userId')
			UTypeId = req.get('userTypeId')
			user = Users.query\
				.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
					Users.UId==UId).first()
			if user:
				if UTypeId:
					user.UTypeId = UTypeId
					db.session.commit()
				response = jsonify({
					"status": 'updated',
					"responseText": user.UName+' '+gettext('successfully updated'),
					})
		elif request.method == 'DELETE':
			req = request.get_json()
			UId = req.get('userId')
			thisUser = Users.query.get(UId)
			thisUser.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": 'deleted',
				"responseText": thisUser.UName+' '+gettext('successfully deleted'),
				})
	except Exception as ex:
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})
	return response