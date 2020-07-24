from flask import render_template,url_for,jsonify,json,session,flash,redirect,request,Response,abort
from flask import current_app
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import commonUsedData
from main_pack.models.commerce.models import Resource
from main_pack.commerce.commerce.utils import UiCategoriesList,uiSortingData
from main_pack.api.commerce.commerce_utils import UiCartResourceData
# / Resource and view /

@bp.route("/v-list")
def v_list():
	page = request.args.get('page',1,type=int)
	pagination_resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc())\
		.paginate(per_page=current_app.config['RESOURCES_PER_PAGE'],page=page)
	product_list = []
	for resource in pagination_resources.items:
		product = {}
		product['ResId'] = resource.ResId
		product_list.append(product)
	res = apiResourceInfo(product_list)
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	return render_template ("commerce/main/commerce/v_list.html",**categoryData,
		**sortingData,**res,title=gettext('Category'),pagination_url='commerce.v_list',
		pagination_resources=pagination_resources)

@bp.route("/v-grid")
def v_grid():
	page = request.args.get('page',1,type=int)
	pagination_resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc())\
		.paginate(per_page=current_app.config['RESOURCES_PER_PAGE'],page=page)
	product_list = []
	for resource in pagination_resources.items:
		product = {}
		product['ResId'] = resource.ResId
		product_list.append(product)
	res = apiResourceInfo(product_list)
	categoryData = UiCategoriesList()
	sortingData = uiSortingData()
	return render_template ("commerce/main/commerce/v_grid.html",**categoryData,
		**sortingData,**res,title=gettext('Category'),pagination_url='commerce.v_grid',
		pagination_resources=pagination_resources)

@bp.route("/product/<int:ResId>")
def product(ResId):
	product_list=[
		{
			'ResId':ResId,
		}
	]
	resData = UiCartResourceData(product_list)
	resource = resData["data"][0]
	categoryData = UiCategoriesList()
	return render_template ("commerce/main/commerce/product.html",
		**categoryData,resource=resource,title=gettext('Product'))
