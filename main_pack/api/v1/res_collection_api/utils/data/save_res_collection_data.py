from uuid import uuid4

from main_pack.api.v1.res_collection_api.utils.data.add_res_collection_dict import add_res_collection_dict, add_res_collection_line_dict
from main_pack.models import (
	Res_collection,
	Res_collection_line,
	Resource,
	Division,
	Company
)

from main_pack import db
from main_pack.base import log_print

def save_res_collection_data(req):
	data, fails = [], []

	for rc_req in req:
		try:
			this_rc_data = add_res_collection_dict(rc_req)

			try:
				this_rc_CGuid = rc_req["CGuid"]
				if this_rc_CGuid:
					this_rc_company = Company.query.filter_by(CGuid = this_rc_CGuid).first()
					if this_rc_company:
						this_rc_data["CId"] = this_rc_company.CId
			except:
				pass
			
			try:
				this_rc_DivGuid = rc_req["DivGuid"]
				if this_rc_DivGuid:
					this_rc_division = Division.query.filter_by(DivGuid = this_rc_DivGuid).first()
					if this_rc_division:
						this_rc_data["DivId"] = this_rc_division.DivId
			except:
				pass

			this_res_collection = Res_collection.query.filter_by(
				ResCollectionGuid = this_rc_data["ResCollectionGuid"]
			).first()

			if this_res_collection:
				this_res_collection.update(**this_rc_data)

			else:
				this_rc_data["ResCollectionGuid"] = uuid4()
				this_res_collection = Res_collection(**this_rc_data)
				db.session.add(this_res_collection)

			success_lines, fail_lines = [], []
			if rc_req["Res_collection_lines"]:
				for line_req in rc_req["Res_collection_lines"]:
					try:
						this_line_data = add_res_collection_line_dict(line_req)
						this_line_data["ResCollectionId"] = this_res_collection.ResCollectionId

						try:
							this_line_res_guid = line_req["ResGuid"]
							if this_line_res_guid:
								this_line_resource = Resource.query.filter_by(ResGuid = this_line_res_guid).first()
								if this_line_resource:
									this_line_data["ResId"] = this_line_resource.ResId
						except:
							pass

						this_rc_line = Res_collection_line.query.filter_by(
							ResCollectionLineGuid = this_line_data["ResCollectionLineGuid"]
						).first()

						if this_rc_line:
							this_rc_line.update(**this_line_data)
						
						else:
							this_line_data["ResCollectionLineGuid"] = uuid4()
							this_rc_line = Res_collection_line(**this_line_data)
							db.session.add(this_rc_line)
						
						success_lines.append(this_rc_line.to_json_api())

					except Exception as ex:
						print(f"ResCollection line exception, {ex}")
						fail_lines.append(line_req)

			res_collection_response = this_res_collection.to_json_api()
			res_collection_response["Res_collection_lines"] = success_lines
			res_collection_response["Res_collection_lines_errors"] = fail_lines
			data.append(res_collection_response)

		except Exception as ex:
			log_print(f"Res_collection_post api: {ex}")
			fails.append(rc_req)

	db.session.commit()

	return data, fails