from uuid import uuid4

from main_pack.api.v1.rating_api.utils.add_Rating_dict import add_Rating_dict
from main_pack.models import Rating, Resource
from main_pack import db
from main_pack.base import log_print


# payload = [
# 	{
# 		"RtRatingValue": 4,
# 		"RtRemark": "skdjhfklsf",
# 		"ResId": 4,
# 		"ResGuid": "asdasdasdasdasdasd-asd-a-sd-asd",
# 	},
# ]

def manage_rating(req, model_type, current_user, method):
	data, fails = [], []

	for req_item in req:
		status, message = 0, "Failed to do that operation"
		try:
			this_req_data = add_Rating_dict(req_item)

			current_filtering = {"GCRecord": None}

			if model_type == "user":
				this_req_data["UId"] = current_user.UId

			if model_type == "rp_acc":
				this_req_data["RpAccId"] = current_user.RpAccId
				this_req_data["RtValidated"] = False
				current_filtering["RpAccId"] = current_user.RpAccId

			ResGuid = None
			if "ResGuid" in req_item:
				ResGuid = req_item["ResGuid"]
			if ResGuid:
				this_resource = Resource.query.filter(Resource.ResGuid == ResGuid).first()
				if this_resource:
					this_req_data["ResId"] = this_resource.ResId
			current_filtering["ResId"] = this_req_data["ResId"]

			if method == "DELETE":
				this_req_data["GCRecord"] = 1

			if model_type == "user":
				RpAccGuid = None
				if "RpAccGuid" in req_item:
					RpAccGuid = req_item["RpAccGuid"]
				if RpAccGuid:
					this_rp_acc = Rp_acc.query.filter(Rp_acc.RpAccGuid == RpAccGuid).first()
					if this_rp_acc:
						this_req_data["RpAccId"] = this_rp_acc.RpAccId
						current_filtering["RpAccId"] = this_rp_acc.RpAccId

			if method != "DELETE":
				if not this_req_data["RtRatingValue"] or not this_req_data["ResId"] or not this_req_data["RtRemark"]:
					log_print(f"Rating api: No rating info or resource specified {req_item}", "warning")
					message = "Wrong or missing credentials like Rating, Remark or Resource"
					status = 0
					raise Exception

			this_rating = Rating.query.filter_by(**current_filtering).first()
			if this_rating:
				if model_type == 'user':
					this_rating.update(**this_req_data)
					message = "Rating updated!" if method != "DELETE" else "Rating deleted"
					status = 1

				elif model_type == 'rp_acc':
					message = "Already rated!"
					status = 2
					if method == "DELETE":
						this_rating.GCRecord = 1
						message = "Rating deleted"
						status = 1

			else:
				if method == "DELETE":
					raise Exception

				this_req_data["RtGuid"] = uuid4()
				this_rating = Rating(**this_req_data)
				db.session.add(this_rating)
				message = "Rating created!"
				status = 1

			this_rating_data = this_rating.to_json_api()
			this_rating_data["status"] = status
			this_rating_data["message"] = message
			data.append(this_rating_data)

		except Exception as ex:
			log_print(f"Rating api exception: {ex}")
			req_item["status"] = status
			req_item["message"] = message
			fails.append(req_item)

	db.session.commit()

	return data, fails