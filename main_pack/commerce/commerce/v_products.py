from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.commerce import bp
from main_pack.config import Config

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from sqlalchemy import and_
# / useful methods / 

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# Resource and view
from main_pack.base.invoiceMethods import resource_config_check
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.models.commerce.models import (Resource,
																							Res_total,
																							Barcode,
																							Rating,
																							Res_category,
																							Res_price)
from main_pack.commerce.commerce.utils import UiCategoriesList,uiSortingData
from main_pack.api.commerce.commerce_utils import UiCartResourceData
# / Resource and view /


def collect_resource_paginate_info(pagination_url,
																	page = 1,
																	per_page = None,
																	filtration = None,
																	category = None):
	filtration_titles = [
		{
			"filtration": "date_new",
			"filtration_Title": gettext("Newest")
		},
		{
			"filtration": "date_old",
			"filtration_Title": gettext("Oldest")
		},
		{
			"filtration": "price_high",
			"filtration_Title": f'{gettext("Price")} {gettext("high to low")}'
		},
		{
			"filtration": "price_low",
			"filtration_Title": f'{gettext("Price")} {gettext("low to high")}'
		},
		{
			"filtration": "rated",
			"filtration_Title": gettext("Rated")
		}
	]
	filtration_Title = None

	resources = Resource.query\
		.filter_by(GCRecord = None, UsageStatusId = 1)\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1, 
			Res_total.ResTotBalance > 0))
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
		for title in filtration_titles:
			if title['filtration'] == filtration:
				filtration_Title = title["filtration_Title"]

	if category:
		category = Res_category.query\
			.filter_by(GCRecord = None)\
			.filter(Res_category.ResCatName.ilike(category))\
			.first()
		if category:
			resources = resources.filter(Resource.ResCatId == category.ResCatId)

	pagination_resources = resources.paginate(per_page=per_page if per_page else Config.RESOURCES_PER_PAGE,page=page)

	resource_models = [resource for resource in pagination_resources.items if pagination_resources.items]
	res = apiResourceInfo(resource_models=resource_models)
	pagination_info = {
		"data": res["data"],
		"total": res["total"],
		"per_page": pagination_resources.per_page,
		"page": pagination_resources.page,
		"pages_total": pagination_resources.pages,
		"next_url": None,
		"prev_url": None,
		"filtration": filtration,
		"filtration_Title": filtration_Title,
		"category": category.ResCatName if category else None
	}
	if pagination_resources.has_next:
		pagination_info["next_url"] = url_for(
			pagination_url,
			page = pagination_resources.next_num,
			per_page = pagination_resources.per_page,
			filter = pagination_info["filtration"],
			category = pagination_info["category"])
	if pagination_resources.has_prev:
		pagination_info["prev_url"] = url_for(
			pagination_url,
			page = pagination_resources.prev_num,
			per_page = pagination_resources.per_page,
			filter = pagination_info["filtration"],
			category = pagination_info["category"])

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
				filter = pagination_info["filtration"],
				category = pagination_info["category"])
		}
		if page_num == pagination_resources.page:
			page_num_info["status"] = "active"
		if not page_num:
			page_num_info["status"] = None
			page_num_info["url"] = None
		page_num_list.append(page_num_info)
	pagination_info["page_num_list"] = page_num_list
	
	return pagination_info


@bp.route(Config.COMMERCE_LIST_VIEW)
def v_list():
	page = request.args.get("page",1,type=int)
	filtration = request.args.get("filter","date",type=str)
	category = request.args.get("category",None,type=str)
	per_page = request.args.get("per_page",None,type=int)
	pagination_url = 'commerce.v_list'
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	pagination_info = collect_resource_paginate_info(
		pagination_url = pagination_url,
		page = page,
		per_page = per_page,
		filtration = filtration,
		category = category)
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_list.html",
		**categoryData,**sortingData,**pagination_info,
		title=gettext(Config.COMMERCE_LIST_VIEW_TITLE))


@bp.route(Config.COMMERCE_GRID_VIEW)
def v_grid():
	page = request.args.get("page",1,type=int)
	filtration = request.args.get("filter","date",type=str)
	category = request.args.get("category",None,type=str)
	per_page = request.args.get("per_page",None,type=int)
	pagination_url = 'commerce.v_grid'
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	pagination_info = collect_resource_paginate_info(
		pagination_url = pagination_url,
		page = page,
		per_page = per_page,
		filtration = filtration,
		category = category)
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_grid.html",
		**categoryData,**sortingData,**pagination_info,
		title=gettext(Config.COMMERCE_GRID_VIEW_TITLE))


@bp.route(Config.COMMERCE_RESOURCE_VIEW+"/<int:ResId>")
def product(ResId):
	product_list=[
		{
			"ResId": ResId,
		}
	]
	try:
		resData = UiCartResourceData(product_list,fullInfo=True,showRelated=True)
		resource = resData["data"][0]
	except:
		abort(404)
	categoryData = UiCategoriesList()

	title =	gettext(Config.COMMERCE_RESOURCE_VIEW_TITLE)
	if Config.RESOURCE_NAME_ON_TITLE == True:
		try:
			title = resource["ResName"]	if resource["ResName"] else ''
		except Exception as ex:
			print(ex)
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/product.html",
		**categoryData,resource=resource,
		title=title)


@bp.route(Config.COMMERCE_SEARCH_VIEW)
def resources_grid_search():
	tag = request.args.get("tag","",type=str)
	searching_tag = "%{}%".format(tag)

	barcodes = Barcode.query\
		.filter(and_(
			Barcode.GCRecord == None,\
			Barcode.BarcodeVal.ilike(searching_tag)))\
		.all()
	
	resources = Resource.query\
		.filter(and_(
			Resource.GCRecord == None,\
			Resource.ResName.ilike(searching_tag),\
			Resource.UsageStatusId == 1))\
		.order_by(Resource.ResId.desc())\
		.all()

	resource_list = []
	if barcodes:
		for barcode in barcodes:
			resource_list.append(barcode.ResId)
	for resource in resources:
		resource_list.append(resource.ResId)

	# removes dublicates
	resource_list = list(set(resource_list))
	resource_list = [{"ResId": resourceId} for resourceId in resource_list]

	resource_models = []
	for resource in resource_list:
		resource_model = Resource.query\
			.filter_by(GCRecord = None, ResId = resource["ResId"], UsageStatusId = 1)\
			.join(Res_total, Res_total.ResId == Resource.ResId)\
			.filter(and_(
				Res_total.WhId == 1, 
				Res_total.ResTotBalance > 0))\
			.first()
		if resource_model:
			resource_models.append(resource_model)
	res = apiResourceInfo(resource_models=resource_models)
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()

	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_search.html",
		**categoryData,**sortingData,**res,searching_tag=tag,
		title=gettext(Config.COMMERCE_SEARCH_VIEW_TITLE))