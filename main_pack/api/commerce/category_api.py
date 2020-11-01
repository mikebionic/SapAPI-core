# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime
from sqlalchemy import and_

from main_pack import db
from main_pack.config import Config
from main_pack.api.auth.api_login import sha_required

from main_pack.models.base.models import Division
from main_pack.models.commerce.models import Res_category,Resource,Res_total
from main_pack.api.commerce.utils import addCategoryDict


@api.route("/tbl-dk-categories/<int:ResCatId>/",methods=['GET'])
def api_category(ResCatId):
	if request.method == 'GET':
		category = Res_category.query.get(ResCatId)
		response = jsonify({'category':category.to_json_api()})
		res = {
			"status": 1,
			"data": category.to_json_api()
		}
		response = make_response(jsonify(res),200)
	return response


@api.route("/tbl-dk-categories/",methods=['GET'])
def api_categories():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		avoidQtyCheckup = request.args.get("avoidQtyCheckup",1,type=int)

		if DivId is None:
			division = Division.query.filter_by(DivGuid = Config.C_MAIN_DIVGUID, GCRecord = None).first()
			DivId = division.DivId if division else 1

		Res_Total_subquery = db.session.query(
			Res_total.ResId,
			db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
			db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))\
		.filter(Res_total.DivId == DivId)\
		.group_by(Res_total.ResId)\
		.subquery()

		categories = Res_category.query\
			.filter_by(GCRecord = None)\
			.join(Resource, Resource.ResCatId == Res_category.ResCatId)\
			.filter(Resource.GCRecord == None)\
			.outerjoin(Res_Total_subquery, Res_Total_subquery.c.ResId == Resource.ResId)

		if avoidQtyCheckup == 0:
			if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:	
				categories = categories\
					.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

		# if DivId:
		# 	categories = categories.filter(Resource.DivId == DivId)
		if notDivId:
			categories = categories.filter(Resource.DivId != notDivId)

		categories = categories.order_by(Res_category.ResCatVisibleIndex.asc()).all()
		res = {
			"status": 1,
			"message": "All categories",
			"data": [category.to_json_api() for category in categories],
			"total": len(categories)
		}
		response = make_response(jsonify(res),200)
	return response
	
	
@api.route("/tbl-dk-categories/",methods=['POST'])
@sha_required
def api_post_categories():
	if request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			categories = []
			failed_categories = [] 
			for category_req in req:
				try:
					new_category = addCategoryDict(category_req)
					category = Res_category.query\
						.filter_by(ResCatName = new_category.ResCatName)\
						.first()
					if not category:
						category = Res_category(**new_category)
						db.session.add(category)
					else:
						category.update(**new_category)
					categories.append(new_category)
				except Exception as ex:
					print(f"{datetime.now()} | Category Api Exception: {ex}")
					failed_categories.append(new_category)
			db.session.commit()
			status = checkApiResponseStatus(categories,failed_categories)
			res = {
				"data": categories,
				"fails": failed_categories,
				"success_total": len(categories),
				"fail_total": len(failed_categories)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)	
	return response


@api.route("/tbl-dk-categories/paginate/",methods=['GET'])
def api_paginated_categories():
	page = request.args.get("page",1,type=int)
	pagination = Res_category.query\
		.filter_by(GCRecord = None)\
		.order_by(Res_category.CreatedDate.desc())\
		.paginate(
			page,per_page = Config.API_OBJECTS_PER_PAGE,
			error_out = False
			)
	categories = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('commerce_api.api_paginated_categories',page=page-1)
	next = None
	if pagination.has_next:
		next = url_for('commerce_api.api_paginated_categories',page=page+1)
	
	res = {
		"status": 1,
		"message": "Categories",
		"data": [category.to_json_api() for category in categories],
		"total": len(categories),
		"prev_url": prev,
		"next_url": next,
		"pages_total": pagination.total
	}
	
	return jsonify(res)
