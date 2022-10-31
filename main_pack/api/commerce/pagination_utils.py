# -*- coding: utf-8 -*-
from flask import url_for, session
from sqlalchemy import and_, or_, extract
from sqlalchemy.orm import joinedload
import requests

# datetime, date-parser
import dateutil.parser
from datetime import datetime
# / datetime, date-parser /

from . import api
from main_pack import db, gettext
from main_pack.config import Config
from .commerce_utils import apiResourceInfo, apiOrderInvInfo
from main_pack.base.priceMethods import price_currency_conversion

# Resource db Models
from main_pack.models import (
	Resource,
	Res_total,
	Barcode,
	Rating,
	Res_category,
	Brand,
	Res_price,
	Res_discount,
)
# / Resource db Models /
from main_pack.models import Order_inv

from main_pack.base import log_print


def collect_resource_paginate_info(
	pagination_url,
	page = 1,
	per_page = None,
	sort = None,
	category = None,
	brand = None,
	from_price = None,
	to_price = None,
	search = None,
	showMain = None,
	limit_by = None,
	DivId = None,
	notDivId = None,
	avoidQtyCheckup = 0,
	showNullPrice = 0,
	showInactive = 0,
	showDiscounts = 0,
	currency_code = None,
):
	if not currency_code:
		if "currency_code" in session:
			currency_code = session["currency_code"] if session["currency_code"] else Config.DEFAULT_VIEW_CURRENCY_CODE

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
			"sort_title": '{} {}'.format(gettext("Brand"), gettext("ascending")),
			"status": 0
		},
		{
			"sort": "brand_desc",
			"sort_title": '{} {}'.format(gettext("Brand"), gettext("descending")),
			"status": 0
		},
		{
			"sort": "category_asc",
			"sort_title": '{} {}'.format(gettext("Category"), gettext("ascending")),
			"status": 0
		},
		{
			"sort": "category_desc",
			"sort_title": '{} {}'.format(gettext("Category"), gettext("descending")),
			"status": 0
		}
	]

	resource_filtering = {
		"GCRecord": None,
	}

	if showInactive == False:
		resource_filtering["UsageStatusId"] = 1

	Res_Total_subquery = db.session.query(
		Res_total.ResId,
		db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
		db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))

	if DivId:
		Res_Total_subquery = Res_Total_subquery\
			.filter(Res_total.DivId == DivId)

	Res_Total_subquery = Res_Total_subquery\
		.group_by(Res_total.ResId)\
		.subquery()

	resource_query = db.session.query(
		Resource,
		Res_Total_subquery.c.ResTotBalance_sum,
		Res_Total_subquery.c.ResPendingTotalAmount_sum)\
	.filter_by(**resource_filtering)\
	.outerjoin(Res_Total_subquery, Resource.ResId == Res_Total_subquery.c.ResId)\
	.order_by(Resource.ResViewCnt.desc())

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
				for subsubcategory in subcategory.subcategory:
					category_ids.append(subsubcategory.ResCatId)

		resource_query = resource_query.filter(Resource.ResCatId.in_(category_ids))

	if from_price:
		print("+++++++++++++++++++ checking price", from_price, currency_code, currency_code != Config.MAIN_CURRENCY_CODE)
		if currency_code != Config.MAIN_CURRENCY_CODE:
			from_price = price_currency_conversion(
				priceValue = from_price,
				from_currency = currency_code,
				to_currency = Config.MAIN_CURRENCY_CODE)["ResPriceValue"]
		resource_query = resource_query.filter(Res_price.ResPriceValue >= from_price)

	if to_price:
		if currency_code != Config.MAIN_CURRENCY_CODE:
			to_price = price_currency_conversion(
				priceValue = to_price,
				from_currency = currency_code,
				to_currency = Config.MAIN_CURRENCY_CODE)["ResPriceValue"]
		resource_query = resource_query.filter(Res_price.ResPriceValue <= to_price)

	if showMain:
		resource_query = resource_query.filter(Resource.IsMain > 0)

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

	if notDivId:
		resource_query = resource_query.filter(Resource.DivId != notDivId)

	if search:
		search = search.strip()
		searching_tag = "%{}%".format(search)
		resource_ids = []

		barcodes_search = Barcode.query\
			.filter(and_(
				Barcode.GCRecord == None,\
				Barcode.BarcodeVal.ilike(searching_tag)))
		if DivId:
			barcodes_search = barcodes_search.filter_by(DivId = DivId)
		if notDivId:
			barcodes_search = barcodes_search.filter(Barcode.DivId != DivId)
		barcodes_search = barcodes_search.all()

		if Config.USE_SMART_SEARCH:
			try:
				r = requests.get(f"{Config.SMART_SEARCH_API_URL}?search={search}")
				smart_search_req = r.json()
				resource_ids = [data["ResId"] for data in smart_search_req["data"] if smart_search_req["data"]]

			except Exception as ex:
				resource_ids = []
				log_print(f"Smart search exception {ex}", "warning")

		if not resource_ids or not Config.USE_SMART_SEARCH:
			if Config.SEARCH_BY_RESOURCE_DESCRIPTION:
				resources_search = Resource.query\
					.filter(and_(
						Resource.GCRecord == None,\
						or_(
							Resource.ResName.ilike(searching_tag),
							Resource.ResDesc.ilike(searching_tag)
						),\
						Resource.UsageStatusId == 1))\
					.order_by(Resource.ResId.desc())

			else:
				resources_search = Resource.query\
					.filter(and_(
						Resource.GCRecord == None,\
						Resource.ResName.ilike(searching_tag),\
						Resource.UsageStatusId == 1))\
					.order_by(Resource.ResId.desc())

			if DivId:
				resources_search = resources_search.filter_by(DivId = DivId)
			if notDivId:
				resources_search = resources_search.filter(Resource.DivId != notDivId)
			resources_search = resources_search.all()
			for resource in resources_search:
				resource_ids.append(resource.ResId)

		if barcodes_search:
			for barcode in barcodes_search:
				resource_ids.append(barcode.ResId)

		# removes duplicates
		resource_ids = list(set(resource_ids))
		resource_ids = [ResId for ResId in resource_ids]

		resource_query = resource_query.filter(Resource.ResId.in_(resource_ids))

	if Config.HIDE_UNDER_ZERO_VISIBLE_CATEGORIES:
		resource_query = resource_query\
			.join(Res_category, Res_category.ResCatId == Resource.ResCatId)\
			.filter(Res_category.ResCatVisibleIndex >= 0)

	if showDiscounts:
		resource_query = resource_query\
			.join(Res_discount, Res_discount.SaleResId == Resource.ResId)\
				.filter(Res_discount.ResDiscIsActive == True)

	resource_query = resource_query.options(
		joinedload(Resource.Image),
		joinedload(Resource.Barcode),
		joinedload(Resource.Rating),
		joinedload(Resource.Res_price),
		joinedload(Resource.Res_total),
		joinedload(Resource.res_category),
		joinedload(Resource.unit),
		joinedload(Resource.brand),
		joinedload(Resource.usage_status),
		joinedload(Resource.Res_discount_SaleResId))

	pagination_resources = resource_query.paginate(per_page=per_page if per_page else Config.RESOURCES_PER_PAGE,page=page)

	resource_models = [resource for resource in pagination_resources.items if pagination_resources.items]
	data = []
	if resource_models:
		data = apiResourceInfo(
			resource_models = resource_models,
			limit_by = limit_by,
			currency_code = currency_code,
		)["data"]

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
	if showDiscounts:
		base_url_info["showDiscounts"] = showDiscounts

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