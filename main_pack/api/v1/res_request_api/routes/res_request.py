# -*- coding: utf-8 -*-
from flask import request

from main_pack.api.v1.res_request_api import api
from main_pack.api.v1.res_request_api.utils import collect_res_request_data, save_res_request_data
from main_pack.api.response_handlers import handle_default_response, handle_instertion_response
from main_pack.api.base.validators import request_is_json

# /res-request/
@api.route("/res-request/")
def v_res_request_get():
	arg_data = {
		"ResRequestId": request.args.get("id",None,type=int),
		"DivId": request.args.get("division",None,type=int),
		"CId": request.args.get("company",None,type=int),
		"ResRequestName": request.args.get("name","",type=str),
		"ResRequestGuid": request.args.get("uuid","",type=str)
	}
	data = collect_res_request_data(**arg_data)

	return handle_default_response(data, message = "Res_request")


@api.route("/res-request/", methods=['POST'])
@request_is_json(request)
def v_res_request_post():
	req = request.get_json()
	data, fails = save_res_request_data(req)
	return handle_instertion_response(data, fails, message="res_request_post")