# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.language_api import api
from main_pack.api.v1.language_api.utils import collect_language_data


@api.route("/languages/", methods=['GET'])
def tbl_language_get():
	arg_data = {
		"LangId": request.args.get('id',None,type=int),
		"LangGuid": request.args.get('uuid','',type=str),
		"LangName": request.args.get('name','',type=str),
		"LangDesc": request.args.get('desc','',type=str)
	}

	data = collect_language_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Language",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)