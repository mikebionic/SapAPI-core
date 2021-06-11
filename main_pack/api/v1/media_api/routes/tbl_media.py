# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.media_api import api
from main_pack.api.v1.media_api.utils import collect_media_data


@api.route("/tbl-media/", methods=['GET'])
def tbl_media_get():
	arg_data = {
		"MediaId": request.args.get("id",None,type=int),
		"MediaTitle": request.args.get("title","",type=str),
		"MediaName": request.args.get("name","",type=str),
		"MediaBody": request.args.get("body","",type=str),
		"MediaAuthor": request.args.get("author","",type=str),
		"MediaIsFeatured": request.args.get("isFeatured",None,type=int),
		"MediaCatId": request.args.get("categoryId",None,type=int),
		"language": request.args.get("language","",type=str),
		"startDate": request.args.get("startDate","",type=str),
		"endDate": request.args.get("endDate","",type=str),
	}

	data = collect_media_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Media",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)