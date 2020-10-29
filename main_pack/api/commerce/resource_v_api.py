# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response,url_for
from main_pack.api.commerce import api
from main_pack import db
from sqlalchemy import and_,or_

# functions
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.api.commerce.pagination_utils import collect_resource_paginate_info
# / functions /

# db Models
from main_pack.models.commerce.models import (Resource,
																							Barcode,
																							Res_price,
																							Res_total)
# / db Models /


@api.route("/v-full-resources/")
def api_v_full_resources():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	res = apiResourceInfo(fullInfo=True,DivId=DivId,notDivId=notDivId)
	response = make_response(jsonify(res),200)
	return response


@api.route("/v-resources/")
def api_v_resources():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	res = apiResourceInfo(DivId=DivId,notDivId=notDivId)
	response = make_response(jsonify(res),200)
	return response


@api.route("/v-resources/<int:ResId>/")
def api_v_resource_info(ResId):
	resource_list = [{"ResId": ResId}]
	res = apiResourceInfo(resource_list,single_object=True,showRelated=True)
	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/tbl-dk-categories/<int:ResCatId>/v-resources/")
def api_category_v_resources(ResCatId):
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	resources = Resource.query.filter_by(GCRecord = None, UsageStatusId = 1, ResCatId = ResCatId)
	if DivId:
		resources = resources.filter_by(DivId = DivId)
	if notDivId:
		resources = resources.filter(Resource.DivId != notDivId)

	resources = resources\
		.join(Res_price, Res_price.ResId == Resource.ResId)\
		.filter(and_(
			Res_price.ResPriceTypeId == 2,
			Res_price.ResPriceValue > 0))\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1, 
			Res_total.ResTotBalance > 0))

	res = apiResourceInfo(resource_query=resources)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/resources/")
def api_resources():
	page = request.args.get("page",1,type=int)
	sort = request.args.get("sort","date_new",type=str)
	per_page = request.args.get("per_page",None,type=int)
	category = request.args.get("category",None,type=int)
	brand = request.args.get("brand",None,type=int)
	
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	
	search = request.args.get("search",None,type=str)
	search = search.strip() if search else None

	pagination_url = 'commerce_api.api_resources'
	res = collect_resource_paginate_info(
		pagination_url = pagination_url,
		page = page,
		per_page = per_page,
		sort = sort,
		category = category,
		brand = brand,
		search = search,
		DivId = DivId,
		notDivId = notDivId)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response