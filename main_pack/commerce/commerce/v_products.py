from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

from main_pack.commerce.commerce.utils import UiResourcesList,commonUsedData,uiSortingData,UiPaginatedResList
from main_pack.commerce.commerce.cart_utils import UiCartResourceData

from main_pack.models.commerce.models import Resource

@bp.route("/v-list")
def v_list():
	page = request.args.get('page',1,type=int)
	pagination_resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
	product_list = []
	for resource in pagination_resources.items:
		product = {}
		product['resId'] = resource.ResId
		product_list.append(product)
	res = UiPaginatedResList(product_list)
	commonData = commonUsedData()
	sortingData = uiSortingData()
	return render_template ("commerce/main/commerce/v_list.html",**commonData,
		**sortingData,**res,title=gettext('Category'),pagination_url='commerce.list_paginate',
		pagination_resources=pagination_resources)

# @bp.route("/v-list")
# def v_list():
# 	res = UiResourcesList()
# 	commonData = commonUsedData()
# 	sortingData = uiSortingData()
# 	return render_template ("commerce/main/commerce/v_list.html",**commonData,
# 		**sortingData,**res,title=gettext('Category'))


@bp.route("/product/<int:resId>")
def product(resId):
	product_list=[
		{
			'resId':resId,
		}
	]
	resData = UiCartResourceData(product_list)
	resource = resData["data"][0]
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/product.html",
		**commonData,resource=resource,title=gettext('Product'))


# @bp.route("/product/<int:resId>")
# def product(resId):
# 	resource = Resource.query.get(resId)
# 	commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	return render_template ("commerce/main/commerce/product.html",
# 		resource=resource,**commonData,**resData,title=gettext('Product'))


@bp.route("/v-grid")
def v_grid():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/v_grid.html",**commonData,title=gettext('Category'))