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
	res = apiResourceInfo(fullInfo=True,DivId=DivId,notDivId=notDivId)
	response = make_response(jsonify(res), 200)
	return response


@api.route("/v-resources/")
def api_v_resources():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	avoidQtyCheckup = request.args.get("avoidQtyCheckup",0,type=int)
	res = apiResourceInfo(
		DivId = DivId,
		notDivId = notDivId,
		avoidQtyCheckup = avoidQtyCheckup)
	response = make_response(jsonify(res), 200)
	return response


@api.route("/v-resources/<int:ResId>/")
def api_v_resource_info(ResId):
	resource_list = [{"ResId": ResId}]
	res = apiResourceInfo(resource_list,single_object=True,showRelated=False)
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

	res = apiResourceInfo(resource_query=resources)
	status_code = 200
	response = make_response(jsonify(res), status_code)
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
	response = make_response(jsonify(res), status_code)
	return response
