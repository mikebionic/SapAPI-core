# -*- coding: utf-8 -*-
from sqlalchemy.orm import joinedload

from main_pack.models import Res_collection
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def collect_res_collection_data(
	ResCollectionId = None,
	DivId = None,
	CId = None,
	ResCollectionName = None,
	ResCollectionGuid = None,
):

	filtering = {"GCRecord": None}

	if DivId:
		filtering["DivId"] = DivId
	if CId:
		filtering["CId"] = CId

	res_collections_query = Res_collection.query.filter_by(**filtering)

	if ResCollectionName:
		res_collections_query = res_collections_query.filter(Res_collection.ResCollectionName.ilike(f"%{ResCollectionName}%"))
	if ResCollectionGuid:
		res_collections_query = res_collections_query.filter(Res_collection.ResCollectionGuid.ilike(f"%{ResCollectionGuid}%"))

	res_collections_query = res_collections_query.options(joinedload(Res_collection.Res_collection_line))
	res_collections_query = res_collections_query.order_by(Res_collection.CreatedDate.desc()).all()

	data = []
	for collection in res_collections_query:
		collection_data = collection.to_json_api()
		res_id_list = [{"ResId": line.ResId} for line in collection.Res_collection_line]
		resources_data = apiResourceInfo(resource_list=res_id_list)
		collection_data["Resources"] = resources_data["data"] if resources_data else []
		collection_data["Res_collection_lines"] = [line.to_json_api() for line in collection.Res_collection_line]
		data.append(collection_data)

	return data