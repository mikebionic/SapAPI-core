# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response,url_for
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.api.commerce import api
from main_pack.config import Config
from sqlalchemy import and_

# functions
from main_pack.api.commerce.commerce_utils import apiResourceInfo
# / functions /

# db Models
from main_pack.models.commerce.models import (Resource,
																							Res_total,
																							Barcode,
																							Rating,
																							Res_category,
																							Brand,
																							Res_price)
# / db Models /


def collect_resource_paginate_info(pagination_url,
																	page = 1,
																	per_page = None,
																	filtration = None,
																	category = None,
																	brand = None):
	filtration_types = [
		{
			"filtration": "date_new",
			"filtration_title": gettext("Newest"),
			"status": 0
		},
		{
			"filtration": "date_old",
			"filtration_title": gettext("Oldest"),
			"status": 0
		},
		{
			"filtration": "price_high",
			"filtration_title": gettext("Price: high to low"),
			"status": 0
		},
		{
			"filtration": "price_low",
			"filtration_title": gettext("Price: low to high"),
			"status": 0
		},
		{
			"filtration": "rated",
			"filtration_title": gettext("Rated"),
			"status": 0
		}
	]
	filtration_title = None

	resources = Resource.query\
		.filter_by(GCRecord = None, UsageStatusId = 1)\
		.join(Res_price, Res_price.ResId == Resource.ResId)\
		.filter(and_(
			Res_price.ResPriceTypeId == 2,
			Res_price.ResPriceValue > 0))\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1, 
			Res_total.ResTotBalance > 0))
	
	if brand:
		brand = Brand.query\
			.filter_by(GCRecord = None)\
			.filter(Brand.BrandName.ilike(brand))\
			.first()
		if brand:
			resources = resources.filter(Resource.BrandId == brand.BrandId)

	if filtration:
		if filtration == "date_new":
			resources = resources.order_by(Resource.CreatedDate.desc())
		if filtration == "date_old":
			resources = resources.order_by(Resource.CreatedDate.asc())
		if filtration == "price_high":
			resources = resources\
				.outerjoin(Res_price, Res_price.ResId == Resource.ResId)\
				.filter(Res_price.ResPriceTypeId == 2 and Res_price.GCRecord == None)\
				.order_by(Res_price.ResPriceValue.desc())
		if filtration == "price_low":
			resources = resources\
				.outerjoin(Res_price, Res_price.ResId == Resource.ResId)\
				.filter(Res_price.ResPriceTypeId == 2 and Res_price.GCRecord == None)\
				.order_by(Res_price.ResPriceValue.asc())
		if filtration == "rated":
			resources = resources\
				.outerjoin(Rating, Rating.ResId == Resource.ResId)\
				.order_by(Rating.RtRatingValue.asc())
		for filtration_type in filtration_types:
			if filtration_type['filtration'] == filtration:
				filtration_type["status"] = 1

	if category:
		category = Res_category.query\
			.filter_by(GCRecord = None)\
			.filter(Res_category.ResCatName.ilike(category))\
			.first()
		if category:
			resources = resources.filter(Resource.ResCatId == category.ResCatId)

	pagination_resources = resources.paginate(per_page=per_page if per_page else Config.RESOURCES_PER_PAGE,page=page)

	resource_models = [resource for resource in pagination_resources.items if pagination_resources.items]
	data = []
	if resource_models:
		res = apiResourceInfo(resource_models=resource_models)
		data = res["data"]
	pagination_info = {
		"data": data,
		"total": len(data),
		"per_page": pagination_resources.per_page,
		"page": pagination_resources.page,
		"pages_total": pagination_resources.pages,
		"next_url": None,
		"prev_url": None,
		"current_filtration": filtration,
		"filtration_types": filtration_types,
		"category": category.ResCatName if category else None,
		"brand": brand.BrandName if brand else None
	}
	if pagination_resources.has_next:
		pagination_info["next_url"] = url_for(
			pagination_url,
			page = pagination_resources.next_num,
			per_page = pagination_resources.per_page,
			filter = pagination_info["current_filtration"],
			category = pagination_info["category"],
			brand = pagination_info["brand"])
	if pagination_resources.has_prev:
		pagination_info["prev_url"] = url_for(
			pagination_url,
			page = pagination_resources.prev_num,
			per_page = pagination_resources.per_page,
			filter = pagination_info["current_filtration"],
			category = pagination_info["category"],
			brand = pagination_info["brand"])

	# method for footer pagination
	page_num_list = []
	for page_num in pagination_resources.iter_pages(left_edge=1,right_edge=1,left_current=2,right_current=3):
		page_num_info = {
			"page": page_num,
			"status": "inactive",
			"url": url_for(
				pagination_url,
				page = page_num,
				per_page = pagination_resources.per_page,
				filter = pagination_info["current_filtration"],
				category = pagination_info["category"],
				brand = pagination_info["brand"])
		}
		if page_num == pagination_resources.page:
			page_num_info["status"] = "active"
		if not page_num:
			page_num_info["status"] = None
			page_num_info["url"] = None
		page_num_list.append(page_num_info)
	pagination_info["page_num_list"] = page_num_list
	
	return pagination_info

