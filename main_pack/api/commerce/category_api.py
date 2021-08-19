# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, url_for
from datetime import datetime

from . import api
from main_pack import db
from main_pack.config import Config

from .utils import addCategoryDict
from .commerce_utils import collect_categories_query
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models import Res_category


@api.route("/tbl-dk-categories/",methods=['GET'])
def api_categories():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		avoidQtyCheckup = request.args.get("avoidQtyCheckup",0,type=int)

		categories = collect_categories_query(
			DivId = DivId,
			notDivId = notDivId,
			avoidQtyCheckup = avoidQtyCheckup)

		categories = categories.all()

		data = [category.to_json_api() for category in categories]

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "All categories",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)
	return response
	
	
@api.route("/tbl-dk-categories/",methods=['POST'])
@request_is_json(request)
@sha_required
def api_post_categories():
	if request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = [] 

		for category_req in req:
			try:
				category_info = addCategoryDict(category_req)

				thisCategory = Res_category.query\
					.filter_by(ResCatName = category_info["ResCatName"], GCRecord = None)\
					.first()

				if thisCategory:
					thisCategory.update(**category_info)

				else:
					thisCategory = Res_category(**category_info)
					db.session.add(thisCategory)

				data.append(category_info)

			except Exception as ex:
				print(f"{datetime.now()} | Category Api Exception: {ex}")
				failed_data.append(category_info)

		db.session.commit()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)	

	return response


@api.route("/tbl-dk-categories/paginate/",methods=['GET'])
def api_paginated_categories():
	page = request.args.get("page",1,type=int)
	pagination = Res_category.query\
		.filter_by(GCRecord = None)\
		.order_by(Res_category.CreatedDate.desc())\
		.paginate(
			page,per_page = Config.API_OBJECTS_PER_PAGE,
			error_out = False)

	data = [category.to_json_api() for category in pagination.items]
	prev = None
	next = None

	if pagination.has_prev:
		prev = url_for('commerce_api.api_paginated_categories',page=page-1)
	if pagination.has_next:
		next = url_for('commerce_api.api_paginated_categories',page=page+1)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Categories",
		"data": data,
		"total": len(data),
		"prev_url": prev,
		"next_url": next,
		"pages_total": pagination.total
	}

	return jsonify(res)