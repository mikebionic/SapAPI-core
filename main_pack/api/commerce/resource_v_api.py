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

	resources = resources.all()
	resource_models = [resource for resource in resources]
	res = apiResourceInfo(resource_models=resource_models)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/v-resources/paginate/")
def api_v_resources_paginate():
	page = request.args.get("page",1,type=int)
	filtration = request.args.get("filter","date",type=str)
	category = request.args.get("category",None,type=str)
	per_page = request.args.get("per_page",None,type=int)
	brand = request.args.get("brand",None,type=str)
	pagination_url = 'commerce.api_v_resources_paginate'
	pagination_info = collect_resource_paginate_info(
		pagination_url = pagination_url,
		page = page,
		per_page = per_page,
		filtration = filtration,
		category = category,
		brand = brand)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response


@api.route("/v-resources/search/")
def api_v_resources_search():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)

	tag = request.args.get("tag","",type=str)
	tag = tag.strip()
	searching_tag = "%{}%".format(tag)

	print(len(tag))
	data = []
	if len(tag) > 3:
		barcodes = Barcode.query\
			.filter(and_(
				Barcode.GCRecord == None,\
				Barcode.BarcodeVal.ilike(searching_tag)))\
		
		resources = Resource.query\
			.filter(and_(
				Resource.GCRecord == None,\
				Resource.ResName.ilike(searching_tag),\
				Resource.UsageStatusId == 1))\
			.order_by(Resource.ResId.desc())\

		if DivId:
			barcodes = barcodes.filter_by(DivId = DivId)
			resources = resources.filter_by(DivId = DivId)
		if notDivId:
			barcodes = barcodes.filter(Barcode.DivId != DivId)
			resources = resources.filter(Resource.DivId != notDivId)

		barcodes = barcodes.all()
		resources = resources.all()

		resource_ids = []
		if barcodes:
			for barcode in barcodes:
				resource_ids.append(barcode.ResId)
		for resource in resources:
			resource_ids.append(resource.ResId)

		# removes duplicates
		resource_ids = list(set(resource_ids))
		resource_ids = [ResId for ResId in resource_ids]

		resource_models = Resource.query\
			.filter_by(GCRecord = None, UsageStatusId = 1)\
			.filter(Resource.ResId.in_(resource_ids))\
			.join(Res_total, Res_total.ResId == Resource.ResId)\
			.filter(and_(
				Res_total.WhId == 1,
				Res_total.ResTotBalance > 0))\
			.all()
		if resource_models:
			res = apiResourceInfo(resource_models=resource_models)
			data = res['data']

	res = {
		"status": 1,
		"message": "Resource search results",
		"data": data,
		"total": len(data)
	}

	response = make_response(jsonify(res),200)
	return response
