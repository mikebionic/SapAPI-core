# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.translation_api import api
from main_pack.api.v1.translation_api.utils import collect_translation_data
from main_pack.api.v1.translation_api.utils.data.save_translation_data import save_translation_data
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.utils import admin_required

@api.route("/v-translations/", methods=['GET'])
def v_translations_get():
	arg_data = {
		"TranslId": request.args.get("id",None,type=int),
		"TranslGuid": request.args.get("uuid","",type=str),
		"ResCatId": request.args.get("categoryId",None,type=int),
		"ColorId": request.args.get("colorId",None,type=int),
		"ProdId": request.args.get("prodId",None,type=int),
		"SlImgId": request.args.get("slImgId",None,type=int),
		"LangId": request.args.get("langId",None,type=int),
		"TranslName": request.args.get("nameText","",type=str),
		"TranslDesc": request.args.get("descText","",type=str),
		"LangName": request.args.get("language","",type=str),
	}

	data = collect_translation_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Translation",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)

@api.route("/v-translations/", methods=['POST'])
@admin_required
@request_is_json(request)
def v_translations_post(user):

	req = request.get_json()

	data, fails = save_translation_data(req)
	status = checkApiResponseStatus(data, fails)

	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails),
	}
	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)