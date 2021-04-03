# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, url_for
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from datetime import datetime
import dateutil.parser

from main_pack import gettext
from .collect_order_inv_data import collect_order_inv_data

# Resource db Models
from main_pack.models import (
	Resource,
	Res_total,
	Barcode,
	Rating,
	Res_category,
	Brand,
	Res_price)
# / Resource db Models /

# Invoice db Models
from main_pack.models import (
	Order_inv,
	Invoice)
# / Invoice db Models /
from main_pack.models import Company, Division, Warehouse
from main_pack.models import Rp_acc, User


def collect_order_inv_paginate_data(
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
		res = collect_order_inv_data(
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