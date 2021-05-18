from flask import jsonify, request
from flask_login import current_user, login_required

from main_pack import db, gettext
from main_pack.commerce.commerce import bp
from main_pack.models import Resource, Wish


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
				"status": 'created',
				"responseText": gettext('Product')+' '+gettext('added to wishlist')
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
				"responseText": gettext('Product')+' '+gettext('removed from wishlist')
			})

	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": 'error',
			"responseText": gettext('Unknown error!'),
			})

	return response
