# -*- coding: utf-8 -*-
from flask import request

from main_pack.api.v1.res_collection_api import api
from main_pack.api.v1.res_collection_api.utils import collect_res_collection_data, save_res_collection_data
from main_pack.api.response_handlers import handle_default_response, handle_instertion_response
from main_pack.api.base.validators import request_is_json

# /res-collections/?name=adventure
@api.route("/res-collections/")
def v_res_collection_get():
	arg_data = {
		"ResCollectionId": request.args.get("id",None,type=int),
		"DivId": request.args.get("division",None,type=int),
		"CId": request.args.get("company",None,type=int),
		"ResCollectionName": request.args.get("name","",type=str),
		"ResCollectionGuid": request.args.get("uuid","",type=str)
	}

	data = collect_res_collection_data(**arg_data)

	return handle_default_response(data, message = "Res_collection")


@api.route("/res-collections/", methods=['POST'])
@request_is_json(request)
def v_res_collection_post():
	req = request.get_json()
	data, fails = save_res_collection_data(req)
	return handle_instertion_response(data, fails, message="res_collection_post")