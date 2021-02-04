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

# Resource and view
from main_pack.models.commerce.models import Resource,Wish
from main_pack.models.users.models import Rp_acc
# / Resource and view /

@bp.route('/product/ui_wishlist/',methods=['POST','DELETE'])
@login_required
def ui_wishlist():
	req = request.get_json()
	ResId = req.get("resId")
	RpAccId = current_user.RpAccId
	try:
		if request.method =="POST":
			wish = Wish.query\
				.filter_by(GCRecord = None, ResId = ResId, RpAccId = RpAccId)\
				.first()
			# avoid double insertion
			if wish:
				raise Exception

			resource = Resource.query\
				.filter_by(GCRecord = None, ResId = ResId)\
				.first()
			if resource is None:
				raise Exception
			
			wish = {
				"RpAccId": RpAccId,
				"ResId": ResId,
			}
			wish = Wish(**wish)
			db.session.add(wish)
			db.session.commit()
			response = jsonify({
				"status": 'added',
				"responseText": gettext('Product')+' '+gettext('successfully saved')
			})
		
		if request.method=="DELETE":
			wish = Wish.query\
				.filter_by(GCRecord = None, ResId = ResId, RpAccId = RpAccId)\
				.first()
			if Wish is None:
				raise Exception

			wish.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": 'deleted',
				"responseText": gettext('Product')+' '+gettext('successfully deleted')
			})

	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})

	return response
