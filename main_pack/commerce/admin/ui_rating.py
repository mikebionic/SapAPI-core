from flask import jsonify, request
from flask_login import current_user, login_required

from . import bp
from .utils import addRatingDict
from main_pack import db, gettext
from main_pack.config import Config
from main_pack.commerce.auth.utils import ui_admin_required
from main_pack.models import Rating


@bp.route('/ui/rating_table/', methods=['POST','DELETE'])
@login_required
@ui_admin_required
def ui_rating_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			rating = addRatingDict(req)
			ratingId = req.get('ratingId')

			if (ratingId == '' or ratingId == None):
				raise Exception

			else:
				thisRating = Rating.query.get(ratingId)
				thisRating.update(**rating)
				db.session.commit()
				response = jsonify({
					"status": "updated",
					"responseText": gettext('Rating')+' '+gettext('successfully updated'),
					})			

		elif request.method == 'DELETE': 
			req = request.get_json()
			ratingId = req.get('ratingId')

			thisRating = Rating.query.get(ratingId)
			thisRating.GCRecord = 1
			db.session.commit()

			response = jsonify({
				"status": "deleted",
				"responseText": gettext('Rating')+' '+gettext('successfully deleted'),
				})

	except Exception as ex:
		response = jsonify({
			"status": "error",
			"responseText": gettext('Unknown error!'),
			})
	return response
