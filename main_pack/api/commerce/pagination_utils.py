# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, url_for
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime, timedelta
# / datetime, date-parser /

from main_pack import db, babel, gettext, lazy_gettext
from main_pack.api.commerce import api
from main_pack.config import Config

# functions
from main_pack.api.commerce.commerce_utils import apiResourceInfo, apiOrderInvInfo
# / functions /

# Resource db Models
from main_pack.models.commerce.models import (
	Resource,
	Res_total,
	Barcode,
	Rating,
	Res_category,
	Brand,
	Res_price)
# / Resource db Models /

# Invoice db Models
from main_pack.models.commerce.models import (
	Order_inv,
	Invoice)
# / Invoice db Models /
from main_pack.models.base.models import Company, Division, Warehouse
from main_pack.models.users.models import Rp_acc, Users

def collect_resource_paginate_info(
	pagination_url,
	page = 1,
	per_page = None,
	sort = None,
	category = None,
	brand = None,
	DivId = None,
	notDivId = None,
	search = None,
	avoidQtyCheckup = 0,
	showNullPrice = False,
	showInactive = False):
	sort_types = [
		{
			"sort": "date_new",
			"sort_title": gettext("Newest"),
			"status": 0
		},
		{
			"sort": "date_old",
			"sort_title": gettext("Oldest"),
			"status": 0
		},
		{
			"sort": "price_high",
			"sort_title": gettext("Price: high to low"),
			"status": 0
		},
		{
			"sort": "price_low",
			"sort_title": gettext("Price: low to high"),
			"status": 0
		},
		{
			"sort": "rated",
			"sort_title": gettext("Rated"),
			"status": 0
		},
		{
			"sort": "brand_asc",
			"sort_title": f'{gettext("Brand")} {gettext("ascending")}',
			"status": 0
		},
		{
			"sort": "brand_desc",
			"sort_title": f'{gettext("Brand")} {gettext("descending")}',
			"status": 0
		},
		{
			"sort": "category_asc",
			"sort_title": f'{gettext("Category")} {gettext("ascending")}',
			"status": 0
		},
		{
			"sort": "category_desc",
			"sort_title": f'{gettext("Category")} {gettext("descending")}',
			"status": 0
		}
	]
	sort_title = None
	
	resource_filtering = {
		"GCRecord": None,
	}
	
	if showInactive == False:
		resource_filtering["UsageStatusId"] = 1
	
	if DivId is None:
		# !!! TODO: This option will live for a while
		avoidQtyCheckup = 1

		division = Division.query\
			.filter_by(DivGuid = Config.C_MAIN_DIVGUID, GCRecord = None)\
			.first()
		DivId = division.DivId if division else 1

	if DivId:
		Res_Total_subquery = db.session.query(
			Res_total.ResId,
			db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
			db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))\
		.filter(Res_total.DivId == DivId)\
		.group_by(Res_total.ResId)\
		.subquery()

	resource_query = db.session.query(
		Resource,
		Res_Total_subquery.c.ResTotBalance_sum,
		Res_Total_subquery.c.ResPendingTotalAmount_sum)\
	.filter_by(**resource_filtering)\
	.outerjoin(Res_Total_subquery, Resource.ResId == Res_Total_subquery.c.ResId)

	if avoidQtyCheckup == 0:
		if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:
			resource_query = resource_query\
				.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

	if showNullPrice == False:
		resource_query = resource_query\
			.join(Res_price, Res_price.ResId == Resource.ResId)\
			.filter(and_(
				Res_price.ResPriceTypeId == 2,
				Res_price.ResPriceValue > 0))

	if brand:
		resource_query = resource_query.filter(Resource.BrandId == brand)
	
	if category:
		categories = Res_category.query\
			.filter_by(ResCatId = category, GCRecord = None)\
			.options(
				joinedload(Res_category.subcategory)\
				.options(joinedload(Res_category.subcategory)))\
			.all()

		category_ids = []
		for res_category in categories:
			category_ids.append(res_category.ResCatId)
			for subcategory in res_category.subcategory:
				category_ids.append(subcategory.ResCatId)
				for category in subcategory.subcategory:
					category_ids.append(category.ResCatId)

		resource_query = resource_query.filter(Resource.ResCatId.in_(category_ids))

	if sort:
		if sort == "date_new":
			resource_query = resource_query.order_by(Resource.CreatedDate.desc())
		if sort == "date_old":
			resource_query = resource_query.order_by(Resource.CreatedDate.asc())
		if sort == "brand_asc":
			resource_query = resource_query.order_by(Resource.BrandId.asc())
		if sort == "brand_desc":
			resource_query = resource_query.order_by(Resource.BrandId.desc())
		if sort == "category_asc":
			resource_query = resource_query.order_by(Resource.ResCatId.asc())
		if sort == "category_desc":
			resource_query = resource_query.order_by(Resource.ResCatId.desc())
		if sort == "price_high":
			resource_query = resource_query.order_by(Res_price.ResPriceValue.desc())
		if sort == "price_low":
			resource_query = resource_query.order_by(Res_price.ResPriceValue.asc())
		if sort == "rated":
			resource_query = resource_query\
				.outerjoin(Rating, Rating.ResId == Resource.ResId)\
				.order_by(Rating.RtRatingValue.asc())
		for sort_type in sort_types:
			if sort_type["sort"] == sort:
				sort_type["status"] = 1
	
	# if DivId:
	# 	resource_query = resource_query.filter_by(DivId = DivId)
	if notDivId:
		resource_query = resource_query.filter(Resource.DivId != notDivId)

	if search:
		search = search.strip()
		searching_tag = "%{}%".format(search)
		barcodes_search = Barcode.query\
			.filter(and_(
				Barcode.GCRecord == None,\
				Barcode.BarcodeVal.ilike(searching_tag)))\
		
		resources_search = Resource.query\
			.filter(and_(
				Resource.GCRecord == None,\
				Resource.ResName.ilike(searching_tag),\
				Resource.UsageStatusId == 1))\
			.order_by(Resource.ResId.desc())\

		if DivId:
			barcodes_search = barcodes_search.filter_by(DivId = DivId)
			resources_search = resources_search.filter_by(DivId = DivId)
		if notDivId:
			barcodes_search = barcodes_search.filter(Barcode.DivId != DivId)
			resources_search = resources_search.filter(Resource.DivId != notDivId)

		barcodes_search = barcodes_search.all()
		resources_search = resources_search.all()

		resource_ids = []
		if barcodes_search:
			for barcode in barcodes_search:
				resource_ids.append(barcode.ResId)
		for resource in resources_search:
			resource_ids.append(resource.ResId)

		# removes duplicates
		resource_ids = list(set(resource_ids))
		resource_ids = [ResId for ResId in resource_ids]

		resource_query = resource_query.filter(Resource.ResId.in_(resource_ids))

	resource_query = resource_query.options(
		joinedload(Resource.Image),
		joinedload(Resource.Barcode),
		joinedload(Resource.Rating),
		joinedload(Resource.Res_price),
		joinedload(Resource.Res_total),
		joinedload(Resource.res_category),
		joinedload(Resource.unit),
		joinedload(Resource.brand),
		joinedload(Resource.usage_status))

	pagination_resources = resource_query.paginate(per_page=per_page if per_page else Config.RESOURCES_PER_PAGE,page=page)

	resource_models = [resource for resource in pagination_resources.items if pagination_resources.items]
	data = []
	if resource_models:
		res = apiResourceInfo(resource_models=resource_models)
		data = res["data"]

	pagination_info = {
		"data": data,
		"total": len(data),
		"per_page": pagination_resources.per_page,
		"DivId": DivId,
		"notDivId": notDivId,
		"page": pagination_resources.page,
		"pages_total": pagination_resources.pages,
		"next_url": None,
		"prev_url": None,
		"current_sort": sort,
		"sort_types": sort_types,
		"category": category if category else None,
		"brand": brand if brand else None,
		"search": search if search else None
	}

	base_url_info = {
		"per_page": pagination_resources.per_page,
		"sort": pagination_info["current_sort"],
	}

	if pagination_info["category"]:
		base_url_info["category"] = pagination_info["category"]
	if pagination_info["brand"]:
		base_url_info["brand"] = pagination_info["brand"]
	if DivId:
		base_url_info["DivId"] = DivId
	if notDivId:
		base_url_info["notDivId"] = notDivId
	if search:
		base_url_info["search"] = search

	if pagination_resources.has_next:
		pagination_info["next_url"] = url_for(
			pagination_url,
			page = pagination_resources.next_num,
			**base_url_info)
	if pagination_resources.has_prev:
		pagination_info["prev_url"] = url_for(
			pagination_url,
			page = pagination_resources.prev_num,
			**base_url_info)

	# method for footer pagination
	page_num_list = []
	for page_num in pagination_resources.iter_pages(left_edge=1,right_edge=1,left_current=2,right_current=3):
		page_num_info = {
			"page": page_num,
			"status": "inactive",
			"url": url_for(
				pagination_url,
				page = page_num,
				**base_url_info)
		}
		if page_num == pagination_resources.page:
			page_num_info["status"] = "active"
		if not page_num:
			page_num_info["status"] = None
			page_num_info["url"] = None
		page_num_list.append(page_num_info)
	pagination_info["page_num_list"] = page_num_list
	
	return pagination_info

def collect_order_inv_paginate_info(
	pagination_url,
	startDate = None,
	endDate = datetime.now(),
	invStatus = None,
	rp_acc_user = None,
	DivId = None,
	notDivId = None,
	page = 1,
	per_page = None,
	sort = None,
	invoices_only = False):

	sort_types = [
		{
			"sort": "date_new",
			"sort_title": gettext("Newest"),
			"status": 0
		},
		{
			"sort": "date_old",
			"sort_title": gettext("Oldest"),
			"status": 0
		},
		{
			"sort": "price_high",
			"sort_title": gettext("Price: high to low"),
			"status": 0
		},
		{
			"sort": "price_low",
			"sort_title": gettext("Price: low to high"),
			"status": 0
		}
	]
	sort_title = None

	order_invoices = Order_inv.query\
		.filter_by(GCRecord = None)

	invoice_filtering = {
		"GCRecord": None
	}
	if invStatus:
		invoice_filtering['InvStatId'] = invStatus
	if rp_acc_user:
		invoice_filtering['RpAccId'] = rp_acc_user.RpAccId

	order_invoices = Order_inv.query\
		.filter_by(**invoice_filtering)
	if DivId:
		order_invoices = order_invoices.filter_by(DivId = DivId)
	if notDivId:
		order_invoices = order_invoices.filter(Order_inv.DivId != notDivId)

	if startDate:
		if (type(startDate) != datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate) != datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)
		order_invoices = order_invoices\
			.filter(and_(
				extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
				extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
				extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))

	if sort:
		if sort == "date_new":
			order_invoices = order_invoices.order_by(Order_inv.OInvDate.desc())
		if sort == "date_old":
			order_invoices = order_invoices.order_by(Order_inv.OInvDate.asc())
		if sort == "price_high":
			order_invoices = order_invoices.order_by(Order_inv.OInvFTotal.desc())
		if sort == "price_low":
			order_invoices = order_invoices.order_by(Order_inv.OInvFTotal.asc())
		for sort_type in sort_types:
			if sort_type["sort"] == sort:
				sort_type["status"] = 1

	pagination_order_invoices = order_invoices\
		.paginate(per_page=per_page if per_page else Config.INVOICES_PER_PAGE,page=page)
	invoice_models = [order_inv for order_inv in pagination_order_invoices.items if pagination_order_invoices.items]

	data = []
	if invoice_models:
		res = apiOrderInvInfo(
			invoice_models = invoice_models,
			invoices_only = invoices_only,
			rp_acc_user = rp_acc_user)
		data = res["data"]

	pagination_info = {
		"data": data,
		"total": len(data),
		"per_page": pagination_order_invoices.per_page,
		"page": pagination_order_invoices.page,
		"pages_total": pagination_order_invoices.pages,
		"next_url": None,
		"prev_url": None,
		"current_sort": sort,
		"sort_types": sort_types
	}

	base_url_info = {
		"startDate": startDate,
		"endDate": endDate,
		"invStatus": invStatus,
		"per_page": pagination_order_invoices.per_page,
		"sort": pagination_info["current_sort"],
		"invoices_only": invoices_only
		# "rp_acc_user": rp_acc_user
	}
	if DivId:
		base_url_info["DivId"] = DivId
	if notDivId:
		base_url_info["notDivId"] = notDivId

	if pagination_order_invoices.has_next:
		pagination_info["next_url"] = url_for(
			pagination_url,
			page = pagination_order_invoices.next_num,
			**base_url_info)
	if pagination_order_invoices.has_prev:
		pagination_info["prev_url"] = url_for(
			pagination_url,
			page = pagination_order_invoices.prev_num,
			**base_url_info)

	page_num_list = []
	for page_num in pagination_order_invoices.iter_pages(left_edge=1,right_edge=1,left_current=2,right_current=3):
		page_num_info = {
			"page": page_num,
			"status": "inactive",
			"url": url_for(
				pagination_url,
				page = page_num,
				**base_url_info)
		}
		if page_num == pagination_order_invoices.page:
			page_num_info["status"] = "active"
		if not page_num:
			page_num_info["status"] = None
			page_num_info["url"] = None
		page_num_list.append(page_num_info)
	pagination_info["page_num_list"] = page_num_list
	
	return pagination_info