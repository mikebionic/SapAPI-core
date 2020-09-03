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
from main_pack.models.commerce.models import Resource,Res_total,Barcode,Rating
from main_pack.commerce.commerce.utils import UiCategoriesList,uiSortingData
from main_pack.api.commerce.commerce_utils import UiCartResourceData
# / Resource and view /

def collect_resource_paginate_info(pagination_url,page,filtration):
	pagination_resources = Resource.query\
		.filter_by(GCRecord = None, UsageStatusId = 1)\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1, 
			Res_total.ResTotBalance > 0))\
		.order_by(Resource.CreatedDate.desc())\
		.paginate(per_page=Config.RESOURCES_PER_PAGE,page=page)
	
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
		"filtration":filtration
	}
	if pagination_resources.has_next:
		pagination_info["next_url"] = url_for(pagination_url,
			page=pagination_resources.next_num,
			filter=filtration)
	if pagination_resources.has_prev:
		pagination_info["prev_url"] = url_for(pagination_url,
			page=pagination_resources.prev_num,
			filter=filtration)

	# method for footer pagination
	page_num_list = []
	for page_num in pagination_resources.iter_pages(left_edge=1,right_edge=1,left_current=2,right_current=3):
		page_num_info = {
			"page": page_num,
			"status": "inactive",
			"url": url_for(pagination_url,page=page_num,filter=filtration)
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
	pagination_url = 'commerce.v_list'
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	pagination_info = collect_resource_paginate_info(pagination_url=pagination_url,page=page,filtration=filtration)
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_list.html",
		**categoryData,**sortingData,**pagination_info,
		title=gettext(Config.COMMERCE_LIST_VIEW_TITLE))

@bp.route(Config.COMMERCE_GRID_VIEW)
def v_grid():
	page = request.args.get("page",1,type=int)
	filtration = request.args.get("filter","date",type=str)
	pagination_url = 'commerce.v_grid'
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	pagination_info = collect_resource_paginate_info(pagination_url=pagination_url,page=page,filtration=filtration)
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
	searching_tag = request.args.get("tag","",type=str)
	searching_tag = "%{}%".format(searching_tag)

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
		**categoryData,**sortingData,**res,
		title=gettext(Config.COMMERCE_SEARCH_VIEW_TITLE))


# searching and sorting in one demo
@bp.route(Config.COMMERCE_LIST_VIEW)
def v_list_search():
	searching_tag = request.args.get("tag",'',type=str)
	searching_tag = "%{}%".format(searching_tag)
	price_low = request.args.get("priceLow",0,type=int)
	price_high = request.args.get("priceHigh",0,type=int)
	price_show_type = request.args.get("priceShowType",1,type=int) # 1 = from high to low
	rating_show_type = request.args.get("ratingShowType",1,type=int) # 1 = from high to low
	newness_show_type = request.args.get("newness",1,type=int) # 1 = from new to old
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

	if not searching_tag or searching_tag == '':
		page = request.args.get("page",1,type=int)
		pagination_resources = Resource.query\
			.filter_by(GCRecord = None, UsageStatusId = 1)\
			.join(Res_total, Res_total.ResId == Resource.ResId)\
			.filter(and_(
				Res_total.WhId == 1, 
				Res_total.ResTotBalance > 0))\
			.order_by(Resource.CreatedDate.desc())\
			.paginate(per_page=Config.RESOURCES_PER_PAGE,page=page)
		product_list = []
		for resource in pagination_resources.items:
			product = {}
			product['ResId'] = resource.ResId
			product_list.append(product)
		res = apiResourceInfo(product_list)

	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_list.html",**categoryData,
		**sortingData,**res,pagination_url='commerce.v_list',
		pagination_resources=pagination_resources,
		title=gettext(Config.COMMERCE_SORT_VIEW_TITLE))