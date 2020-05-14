from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.commerce.commerce.utils import commonUsedData,realResRelatedData
from main_pack.models.commerce.models import Resource

@bp.route("/")
def commerce():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/commerce.html",**commonData)

@bp.route("/collection")
def collection():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/collection.html",**commonData,title=gettext('Collection'))

@bp.route("/about")
def about():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/about.html",**commonData,title=gettext('About us'))

@bp.route("/contact")
def contact():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/contact.html",**commonData,title=gettext('Contact'))

@bp.route("/cart")
def cart():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/cart.html",**commonData,title=gettext('Cart'))

@bp.route("/product")
def product_ol():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/product_ol.html",**commonData,title=gettext('Product'))

@bp.route("/category_list")
def category_list():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/category_list.html",**commonData,title=gettext('Category'))

@bp.route("/category_grid")
def category_grid():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/category_grid.html",**commonData,title=gettext('Category'))



############ tests ############
@bp.route("/commerce_test")
def commerce_test():
	resources = Resource.query.order_by(Resource.CreatedDate.desc())
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/commerce_test.html",
		resources=resources,**commonData,**resData)

@bp.route("/list_view")
def list_view():
	resources = Resource.query.order_by(Resource.CreatedDate.desc())
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/list_view.html",
		resources=resources,**commonData,**resData,title=gettext('Category'))

@bp.route("/grid_view")
def grid_view():
	resources = Resource.query.order_by(Resource.CreatedDate.desc())
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/grid_view.html",
		resources=resources,**commonData,**resData,title=gettext('Category'))






#  pagiantions ########
@bp.route("/list_paginate")
def list_paginate():
	page = request.args.get('page',1,type=int)
	resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/list_paginate.html",
		resources=resources,**commonData,**resData,title=gettext('Category'))

@bp.route("/grid_paginate")
def grid_paginate():
	page = request.args.get('page',1,type=int)
	resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/grid_paginate.html",
		resources=resources,**commonData,**resData,title=gettext('Category'))


@bp.route("/products/<string:category>")
def category_product(category):
	page = request.args.get('page',1,type=int)
	resources = Resource.query.filter_by(ResCatName=category)\
		.order_by(Resource.CreatedDate.desc())\
		.paginate(per_page=5,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/grid_view.html",
		resources=resources,**commonData,**resData,title=gettext('Category'))



@bp.route("/product/<int:resId>")
def product(resId):
	resource = Resource.query.get(resId)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/product.html",
		resource=resource,**commonData,**resData,title=gettext('Product'))
