from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.commerce import bp
from main_pack.config import Config

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
# / useful methods / 

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# Resource and view
from main_pack.base.invoiceMethods import resource_config_check
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.models.commerce.models import (
	Resource,
	Res_total,
	Barcode,
	Rating,
	Res_category,
	Brand,
	Res_price)
from main_pack.commerce.commerce.utils import UiCategoriesList,uiSortingData
from main_pack.api.commerce.commerce_utils import UiCartResourceData
from main_pack.api.commerce.pagination_utils import collect_resource_paginate_info
# / Resource and view /


@bp.route(Config.COMMERCE_LIST_VIEW)
def v_list():
	args_data = {
		"page": request.args.get("page",1,type=int),
		"sort": request.args.get("sort","date_new",type=str),
		"per_page": request.args.get("per_page",None,type=int),
		"category": request.args.get("category",None,type=int),
		"brand": request.args.get("brand",None,type=int),
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"pagination_url": 'commerce.v_list'
	}
	search = request.args.get("search",None,type=str)
	args_data["search"] = search.strip() if search else None
	pagination_info = collect_resource_paginate_info(**args_data)

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}commerce/v_list.html",
		**categoryData,**pagination_info,
		title=gettext(Config.COMMERCE_LIST_VIEW_TITLE))


@bp.route(Config.COMMERCE_GRID_VIEW)
def v_grid():
	args_data = {
		"page": request.args.get("page",1,type=int),
		"sort": request.args.get("sort","date_new",type=str),
		"per_page": request.args.get("per_page",None,type=int),
		"category": request.args.get("category",None,type=int),
		"brand": request.args.get("brand",None,type=int),
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"pagination_url": 'commerce.v_grid'
	}
	search = request.args.get("search",None,type=str)
	args_data["search"] = search.strip() if search else None
	pagination_info = collect_resource_paginate_info(**args_data)

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}commerce/v_grid.html",
		**categoryData,**pagination_info,
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
	# remove leading and trailing spaces
	tag = tag.strip()
	searching_tag = "%{}%".format(tag)
	if tag == "" or len(tag) < 3:
		return redirect(url_for('commerce.v_grid'))
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
	
	resource_ids = []
	if barcodes:
		for barcode in barcodes:
			resource_ids.append(barcode.ResId)
	for resource in resources:
		resource_ids.append(resource.ResId)

	# removes duplicates
	resource_ids = list(set(resource_ids))
	resource_ids = [ResId for ResId in resource_ids]

	resources = Resource.query\
		.filter_by(GCRecord = None, UsageStatusId = 1)\
		.filter(Resource.ResId.in_(resource_ids))\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1,
			Res_total.ResTotBalance > 0))

	res = apiResourceInfo(resource_query=resources)

	categoryData = UiCategoriesList()
	sortingData = uiSortingData()

	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_search.html",
		**categoryData,**sortingData,**res,searching_tag=tag,
		title=gettext(Config.COMMERCE_SEARCH_VIEW_TITLE))