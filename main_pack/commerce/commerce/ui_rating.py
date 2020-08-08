from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.commerce import bp
import os
from flask import current_app

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from sqlalchemy import and_
# / useful methods /

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# db Models
from main_pack.models.commerce.models import Resource,Rating
from main_pack.models.users.models import Rp_acc
# / db Models /

@bp.route('/product/ui_rating/',methods=['POST','DELETE'])
@login_required
def ui_rating():
	req = request.get_json()
	ResId = req.get("resId")
	RpAccId = current_user.RpAccId
	try:
		if request.method =="POST":
			# # check for presense of rp_acc (optional step)
			# rp_acc = Rp_acc.query\
			# 	.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
			# 		Rp_acc.RpAccId==RpAccId).first()
			# if rp_acc is None:
			# 	raise Exception
			RtRatingValue = req.get("ratingValue")
			RtRemark = req.get("ratingRemark")
			if RtRatingValue is None:
				raise Exception
			# check for presense of rate
			rating = Rating.query\
				.filter_by(GCRecord = None, ResId = ResId, RpAccId = RpAccId)\
				.first()
			# avoid double insertion
			if rating:
				raise Exception

			resource = Resource.query\
				.filter_by(GCRecord = None, ResId = ResId)\
				.first()
			# avoid insertion of Deleted or null resource
			if resource is None:
				raise Exception
			
			rating = {
				"RpAccId": RpAccId,
				"ResId": ResId,
				"RtRatingValue": RtRatingValue,
				"RtRemark": RtRemark
			}
			rating = Rating(**rating)
			db.session.add(rating)
			db.session.commit()
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Rating')+' '+gettext('successfully saved')
			})
		
		if request.method=="DELETE":
			rating = Rating.query\
				.filter_by(GCRecord = None, ResId = ResId, RpAccId = RpAccId)\
				.first()
			if Rating is None:
				raise Exception

			rating.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": 'deleted',
				"responseText": gettext('Rating')+' '+gettext('successfully deleted')
			})

	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})

	return response
