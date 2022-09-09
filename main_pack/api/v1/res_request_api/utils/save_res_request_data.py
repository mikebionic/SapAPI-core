from uuid import uuid4

from main_pack.api.v1.res_request_api.utils.add_res_request_dict import add_res_request_dict
from main_pack.models import Res_request


from main_pack import db
from main_pack.base import log_print

def save_res_request_data(req):
	data, fails = [], []
	print(req)

	for res_req in req:
		try:
			this_rc_data = add_res_request_dict(res_req)

			this_res_request = Res_request.query.filter_by(
				ResReqGuid = this_rc_data["ResReqGuid"]
			).first()

			if this_res_request:
				this_res_request.update(**this_rc_data)

			else:
				this_rc_data["ResReqGuid"] = uuid4()
				this_res_request = Res_request(**this_rc_data)
				db.session.add(this_res_request)

		except Exception as ex:
			log_print(f"Res_request_post api: {ex}")
			fails.append(res_req)

	db.session.commit()

	return data, fails