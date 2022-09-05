# -*- coding: utf-8 -*-
from sqlalchemy.orm import joinedload

from main_pack.models import Res_request
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def collect_res_request_data(
	ResCollectionId = None,
	DivId = None,
	CId = None,
	ResRequestName = None,
	ResRequestGuid = None,
):

	filtering = {"GCRecord": None}

	if DivId:
		filtering["DivId"] = DivId
	if CId:
		filtering["CId"] = CId

	res_request_query = Res_request.query.filter_by(**filtering)

	if ResRequestName:
		res_request_query = res_request_query.filter(Res_request.ResRequestName.ilike(f"%{ResRequestName}%"))
	if ResRequestGuid:
		res_request_query = res_request_query.filter(Res_request.ResRequestGuid.ilike(f"%{ResRequestGuid}%"))

	# res_request_query = res_request_query.options(joinedload(Res_request.Res_collection_line))
	# res_request_query = res_request_query.order_by(Res_request.CreatedDate.desc()).all()

	data = []
	for request in res_request_query:
		request_data = request.to_json_api()
		res_id_list = [{"ResId": line.ResId} for line in request.Res_collection_line if line.ResId if line]
		resources_data = apiResourceInfo(resource_list=res_id_list)
		request_data["Resources"] = resources_data["data"] if resources_data else []

		lines_list = []
		# for line in request.Res_collection_line:
		# 	this_line_data = line.to_json_api()
		# 	for resource in resources_data["data"]:
		# 		if resource["ResId"] == line.ResId:
		# 			this_line_data["ResName"] = resource["ResName"]
		# 			this_line_data["ResGuid"] = resource["ResGuid"]
		# 	lines_list.append(this_line_data)

		request_data["Res_collection_lines"] = lines_list


		data.append(request_data)

	return data