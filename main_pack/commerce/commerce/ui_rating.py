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
			RtRatingValue = req.get("ratingValue")
			RtRemark = req.get("ratingRemark")
			RtRemark = RtRemark.strip()
			if RtRatingValue is None or len(RtRemark) <= 2:
				raise Exception
			# # check for presense of rate
			# rating = Rating.query\
			# 	.filter_by(GCRecord = None, ResId = ResId, RpAccId = RpAccId)\
			# 	.first()
			# # avoid double insertion
			# if rating:
			# 	raise Exception

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
				"status": 'updated',
				"responseText": gettext('Rating') + ' ' + gettext('successfully sent') + '. ' + gettext('It will be shown after some time')
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
