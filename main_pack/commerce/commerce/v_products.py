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

@bp.route(Config.COMMERCE_LIST_VIEW)
def v_list():
	url_prefix = request.url_rule.rule
	page = request.args.get('page',1,type=int)
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
		title=gettext(Config.COMMERCE_LIST_VIEW_TITLE))

@bp.route(Config.COMMERCE_GRID_VIEW)
def v_grid():
	page = request.args.get('page',1,type=int)
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
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/v_grid.html",**categoryData,
		**sortingData,**res,pagination_url='commerce.v_grid',
		pagination_resources=pagination_resources,
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

@bp.route(Config.COMMERCE_LIST_VIEW+"/search")
def resources_list_search():
	searching_tag = request.args.get('tag',"",type=str)
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

	res = apiResourceInfo(resource_list)

	res = {
		"status": 1,
		"message": "Resource search results",
		"data": res['data'],
		"total": len(resource_list)
	}

	response = make_response(jsonify(res),200)
	return response

# searching and sorting in one demo
@bp.route(Config.COMMERCE_LIST_VIEW)
def v_list_search():
	searching_tag = request.args.get('tag','',type=str)
	searching_tag = "%{}%".format(searching_tag)
	price_low = request.args.get('priceLow',0,type=int)
	price_high = request.args.get('priceHigh',0,type=int)
	price_show_type = request.args.get('priceShowType',1,type=int) # 1 = from high to low
	rating_show_type = request.args.get('ratingShowType',1,type=int) # 1 = from high to low
	newness_show_type = request.args.get('newness',1,type=int) # 1 = from new to old
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
		page = request.args.get('page',1,type=int)
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