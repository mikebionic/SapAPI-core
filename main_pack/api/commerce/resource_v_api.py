# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, url_for
from sqlalchemy import and_,or_

from . import api
from main_pack import db
from main_pack.config import Config

from .commerce_utils import apiResourceInfo
from .pagination_utils import collect_resource_paginate_info

from main_pack.models import Division
from main_pack.models import (
	Resource,
	Barcode,
	Res_price,
	Res_total
)


@api.route("/v-full-resources/")
def api_v_full_resources():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	showMain = request.args.get("showMain",0,type=int)
	limit_by = request.args.get("limit",None,type=int)
	res = apiResourceInfo(
		fullInfo = True,
		DivId = DivId,
		notDivId = notDivId,
		showMain = showMain,
		limit_by = limit_by)
	response = make_response(jsonify(res), 200)
	return response


@api.route("/v-resources/")
def api_v_resources():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	avoidQtyCheckup = request.args.get("avoidQtyCheckup",0,type=int)
	showMain = request.args.get("showMain",0,type=int)
	limit_by = request.args.get("limit",None,type=int)
	showImage = request.args.get("showImage",1,type=int)
	showLastVendor = request.args.get("showLastVendor",0,type=int)
	showPurchacePrice = request.args.get("showPurchacePrice",0,type=int)	
	search = request.args.get("search",None,type=str)
	search = search.strip() if search else None

	res = apiResourceInfo(
		DivId = DivId,
		notDivId = notDivId,
		avoidQtyCheckup = avoidQtyCheckup,
		showMain = showMain,
		limit_by = limit_by,
		showImage = showImage,
		showLastVendor = showLastVendor,
		showPurchacePrice = showPurchacePrice,
		search = search,
	)
	return make_response(jsonify(res), 200)


@api.route("/v-resources/<int:ResId>/")
def api_v_resource_info(ResId):
	resource_list = [{"ResId": ResId}]
	showRelated = request.args.get("showRelated",0,type=int)
	showRatings = request.args.get("showRatings",0,type=int)
	res = apiResourceInfo(
		resource_list,
		single_object = True,
		showRelated = showRelated,
		showRatings = showRatings
	)
	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res), status_code)
	return response


@api.route("/tbl-dk-categories/<int:ResCatId>/v-resources/")
def api_category_v_resources(ResCatId):
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	avoidQtyCheckup = request.args.get("avoidQtyCheckup",0,type=int)
	showMain = request.args.get("showMain",0,type=int)
	limit_by = request.args.get("limit",None,type=int)
	# fetching total by division 
	if DivId is None:
		# !!! TODO: This option will live for a while
		avoidQtyCheckup = 1

		division = Division.query.filter_by(DivGuid = Config.C_MAIN_DIVGUID).first()
		DivId = division.DivId if division else 1

	if DivId:
		Res_Total_subquery = db.session.query(
			Res_total.ResId,
			db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
			db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))\
		.filter(Res_total.DivId == DivId)\
		.group_by(Res_total.ResId)\
		.subquery()

	resources = db.session.query(
		Resource, 
		Res_Total_subquery.c.ResTotBalance_sum,
		Res_Total_subquery.c.ResPendingTotalAmount_sum)\
	.filter_by(GCRecord = None, UsageStatusId = 1, ResCatId = ResCatId)

	#if DivId:
	#	resources = resources.filter_by(DivId = DivId)
	if notDivId:
		resources = resources.filter(Resource.DivId != notDivId)

	resources = resources\
		.join(Res_price, Res_price.ResId == Resource.ResId)\
		.filter(and_(
			Res_price.ResPriceTypeId == 2,
			Res_price.ResPriceValue > 0))

	resources = resources\
		.outerjoin(Res_Total_subquery, Resource.ResId == Res_Total_subquery.c.ResId)
	if avoidQtyCheckup == 0:
		if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:	
			resources = resources\
				.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

	res = apiResourceInfo(
		resource_query=resources,
		showMain=showMain,
		limit_by = limit_by)
	status_code = 200
	response = make_response(jsonify(res), status_code)
	return response


#  /resources/?brand=1&category=2&sort
@api.route("/resources/")
def api_resources():
	page = request.args.get("page",1,type=int)
	sort = request.args.get("sort","date_new",type=str)
	per_page = request.args.get("per_page",None,type=int)
	category = request.args.get("category",None,type=int)
	brand = request.args.get("brand",None,type=int)
	from_price = request.args.get("from_price",None,type=float)
	to_price = request.args.get("to_price",None,type=float)

	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	showMain = request.args.get("showMain",0,type=int)
	limit_by = request.args.get("limit",0,type=int)
	showDiscounts = request.args.get("showDiscounts",0,type=int)

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
		from_price = from_price,
		to_price = to_price,
		search = search,
		showMain = showMain,
		limit_by = limit_by,
		DivId = DivId,
		notDivId = notDivId,
		showDiscounts = showDiscounts,
	)

	status_code = 200
	res["status"] = 1
	response = make_response(jsonify(res), status_code)
	return response
