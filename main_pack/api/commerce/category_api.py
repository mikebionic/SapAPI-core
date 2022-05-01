# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, url_for, session
from datetime import datetime
from sqlalchemy.orm import joinedload

from . import api
from main_pack import db, cache
from main_pack.config import Config

from .utils import addCategoryDict
from .commerce_utils import collect_categories_query
from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.response_handlers import handle_default_response

from main_pack.models import Res_category


@api.route("/tbl-dk-categories/")
def api_categories():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		avoidQtyCheckup = request.args.get("avoidQtyCheckup",0,type=int)
		showNullResourceCategory = request.args.get("showNullResourceCategory",0,type=int)

		categories = collect_categories_query(
			DivId = DivId,
			notDivId = notDivId,
			avoidQtyCheckup = avoidQtyCheckup,
			showNullResourceCategory = showNullResourceCategory)

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
@admin_required
def api_post_categories(user):
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


@api.route("/tbl-dk-categories/paginate/")
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



@api.route("/v-categories/")
def v_categories():
	language_code = request.args.get("language","",type=str)
	data = view_categories(language_code)
	return handle_default_response(data, message="Categories")

@cache.cached(Config.DB_CACHE_TIME, key_prefix="v_categories")
def view_categories(language_code = None):
	if not language_code:
		if "language" in session:
			language_code = session["language"] if session["language"] else Config.BABEL_DEFAULT_LOCALE

	categories = collect_categories_query(
		showNullResourceCategory = Config.SHOW_NULL_RESOURCE_CATEGORY,
	).options(joinedload(Res_category.Resource))
	if Config.SHOW_RES_TRANSLATIONS:
		categories = categories.options(joinedload(Res_category.Translation))
	categories = categories.all()

	main_categories = []
	last_categories = []
	for category in categories:
		if not category.ResOwnerCatId:
			if (category.ResCatVisibleIndex > 0):
				main_categories.append(category)
			else:
				last_categories.append(category)

	if last_categories:
		for category in last_categories:
			main_categories.append(category)

	categories_list = []

	for main_category in main_categories:
		subcategories = [category for category in main_category.subcategory if not category.GCRecord]

		data = []
		for subcategory in subcategories:
			category_data = subcategory.to_json_api()
			category_data = configure_res_translation(subcategory, category_data, language_code)

			subcategory_children = [category.to_json_api() for category in subcategory.subcategory if not category.GCRecord]
			category_data["Categories"] = subcategory_children
			data.append(category_data)

		category_data = main_category.to_json_api()
		category_data = configure_res_translation(main_category, category_data, language_code)

		category_data["Categories"] = data
		categories_list.append(category_data)
	return categories_list


def configure_res_translation(
	category_model,
	category_data,
	language_code = Config.BABEL_DEFAULT_LOCALE,
):
	if Config.SHOW_RES_TRANSLATIONS:
		if category_model.Translation and language_code:
			for this_transl in category_model.Translation:
				if language_code in this_transl.language.LangName:
					if this_transl.TranslName:
						category_data["ResCatName"] = this_transl.TranslName
					if this_transl.TranslDesc:
						category_data["ResCatDesc"] = this_transl.TranslDesc

	return category_data

