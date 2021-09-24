from flask import render_template,request,abort


from . import bp, url_prefix
from main_pack import gettext
from main_pack.config import Config

from main_pack.commerce.commerce.utils import UiCategoriesList, UiBrandsList
from main_pack.api.commerce.commerce_utils import UiCartResourceData
from main_pack.api.commerce.pagination_utils import collect_resource_paginate_info


@bp.route(Config.COMMERCE_LIST_VIEW)
@bp.route(f"{Config.COMMERCE_LIST_VIEW}/category-<int:ResCatId>/<ResCatName>")
@bp.route(f"{Config.COMMERCE_LIST_VIEW}/brand-<int:BrandId>/<BrandName>")
def v_list(
	ResCatId = None,
	ResCatName = None,
	BrandId = None,
	BrandName = None,
):
	args_data = {
		"page": request.args.get("page",1,type=int),
		"sort": request.args.get("sort","date_new",type=str),
		"per_page": request.args.get("per_page",None,type=int),
		"category": ResCatId if ResCatId else request.args.get("category",None,type=int),
		"brand": BrandId if BrandId else request.args.get("brand",None,type=int),
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"pagination_url": 'commerce.v_list'
	}
	search = request.args.get("search",None,type=str)
	args_data["search"] = search.strip() if search else None

	pagination_info = collect_resource_paginate_info(**args_data)

	res = {}

	if Config.COMMERCE_SHOW_BRANDS_ON_RESOURCES_PAGE:
		brands = UiBrandsList()
		res["Brands"] = brands["data"]

	categoryData = UiCategoriesList()

	title = None
	if ResCatName:
		title = ResCatName
	if BrandName:
		title = BrandName
	if search:
		title = f"Search: {search.strip()}"

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/v_list.html",
		**categoryData,
		**pagination_info,
		**res,
		url_prefix = url_prefix,
		title = title if title else gettext(Config.COMMERCE_LIST_VIEW_TITLE))


@bp.route(Config.COMMERCE_GRID_VIEW)
@bp.route(f"{Config.COMMERCE_GRID_VIEW}/category-<int:ResCatId>/<ResCatName>")
@bp.route(f"{Config.COMMERCE_GRID_VIEW}/brand-<int:BrandId>/<BrandName>")
def v_grid(
	ResCatId = None,
	ResCatName = None,
	BrandId = None,
	BrandName = None,
):
	args_data = {
		"page": request.args.get("page",1,type=int),
		"sort": request.args.get("sort","date_new",type=str),
		"per_page": request.args.get("per_page",None,type=int),
		"category": ResCatId if ResCatId else request.args.get("category",None,type=int),
		"brand": BrandId if BrandId else request.args.get("brand",None,type=int),
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"pagination_url": 'commerce.v_grid'
	}
	search = request.args.get("search",None,type=str)
	args_data["search"] = search.strip() if search else None

	pagination_info = collect_resource_paginate_info(**args_data)

	res = {}

	if Config.COMMERCE_SHOW_BRANDS_ON_RESOURCES_PAGE:
		brands = UiBrandsList()
		res["Brands"] = brands["data"]

	categoryData = UiCategoriesList()

	title = None
	if ResCatName:
		title = ResCatName
	if BrandName:
		title = BrandName
	if search:
		title = f"Search: {search.strip()}"

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/v_grid.html",
		**categoryData,
		**pagination_info,
		**res,
		url_prefix = url_prefix,
		title = title if title else gettext(Config.COMMERCE_GRID_VIEW_TITLE))


@bp.route(Config.COMMERCE_RESOURCE_VIEW+"/<int:ResId>")
@bp.route(Config.COMMERCE_RESOURCE_VIEW+"/<int:ResId>/<ResName>")
def product(ResId, ResName = None):
	product_list=[
		{
			"ResId": ResId,
		}
	]

	try:
		resData = UiCartResourceData(
			product_list,
			fullInfo = True,
			showRelated = True,
		)
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

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/product.html",
		**categoryData,
		resource = resource,
		url_prefix = url_prefix,
		handle_product_view = Config.HANDLE_PRODUCT_VIEW,
		view_handler_api_url = Config.VIEW_HANDLER_API_URL,
		title = title)