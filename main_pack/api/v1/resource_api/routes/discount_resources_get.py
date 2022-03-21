# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.resource_api import api
from main_pack.api.v1.resource_api.utils import collect_discount_resource_data


@api.route("/discount-resources/", methods=['GET'])
def discount_resources_get():
	limit = request.args.get("limit", None, type=int)
	showInactive = request.args.get("showInactive", None, type=int)

	data = collect_discount_resource_data(limit, showInactive)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "resource",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)