from uuid import uuid4

from main_pack.api.v1.rating_api.utils.data.add_Rating_dict import add_Rating_dict
from main_pack.models import Language, Rating, Resource
from main_pack import db
from main_pack.base import log_print




	# ResId = req.get("resId")
	# rating_filtering = {"GCRecord": None, "ResId": ResId}

	# try:
	# 	if(current_user.is_authenticated and "model_type" in session):
	# 		if session["model_type"] == "rp_acc":
	# 			rating_filtering["RpAccId"] = current_user.RpAccId
	# 		elif session["model_type"] == "user":
	# 			rating_filtering["UId"] == current_user.UId

	# 	if request.method =="POST":
	# 		RtRatingValue = req.get("ratingValue")
	# 		RtRemark = req.get("ratingRemark")
	# 		RtRemark = RtRemark.strip()

	# 		if RtRatingValue is None or len(RtRemark) <= 2:
	# 			raise Exception

	# 		# check for presense of rate
	# 		rating = Rating.query\
	# 			.filter_by(**rating_filtering)\
	# 			.first()

	# 		if rating:
	# 			response = jsonify({
	# 				"status": 'error',
	# 				"responseText": "{} {}.".format(gettext('Rating'), gettext('already sent'))
	# 			})
	# 			return response

	# 		resource = Resource.query\
	# 			.filter_by(GCRecord = None, ResId = ResId)\
	# 			.first()
	# 		# avoid insertion of Deleted or null resource
	# 		if resource is None:
	# 			raise Exception
			
	# 		rating = {
	# 			**rating_filtering,
	# 			"RtRatingValue": RtRatingValue,
	# 			"RtRemark": RtRemark
	# 		}
	# 		rating = Rating(**rating)
	# 		db.session.add(rating)
	# 		db.session.commit()

	# 		response = jsonify({
	# 			"status": 'updated',
	# 			"responseText": "{} {}. {}".format(gettext('Rating'), gettext('successfully sent'), gettext('It will be shown after some time'))
	# 		})
		
	# 	if request.method=="DELETE":
	# 		rating = Rating.query\
	# 			.filter_by(**rating_filtering)\
	# 			.first()
	# 		if Rating is None:
	# 			raise Exception

	# 		rating.GCRecord = 1
	# 		db.session.commit()
	# 		response = jsonify({
	# 			"status": 'deleted',
	# 			"responseText": gettext('Rating')+' '+gettext('successfully deleted')
	# 		})

	# except Exception as ex:
	# 	print(ex)
	# 	response = jsonify({
	# 		"status": 'error',
	# 		"responseText": gettext('Unknown error!'),
	# 		})







def manage_rating(req, model_type, current_user, method):
	data, fails = [], []

	for req_item in req:
		try:
			this_req_data = add_Rating_dict(req_item)
			
			rating_filtering = {"GCRecord": None}
			
			ResGuid = req_item["ResGuid"]
			if ResGuid:
				this_resource = Resource.query.filter(Resource.ResGuid == ResGuid).first()
				if this_resource:
					this_req_data["ResId"] = this_resource.ResId

			if not this_req_data["RatingValue"] or not this_req_data["ResId"] or not this_req_data["RatingRtRemark"]:
				log_print(f"Rating api: No rating info or resource specified {req_item}", "warning")
				raise Exception

			this_translation = Rating.query.filter_by(
				LangId = this_req_data["LangId"],
				ResId = this_req_data["ResId"],
			).first()

			if this_translation:
				this_translation.update(**this_req_data)

			else:
				this_req_data["ResTranslGuid"] = uuid4()
				this_translation = Rating(**this_req_data)
				db.session.add(this_translation)

			data.append(this_translation.to_json_api())

		except Exception as ex:
			log_print(f"Translations api: {ex}")
			fails.append(req_item)

	db.session.commit()

	return data, fails