from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.commerce.commerce.utils import commonUsedData,realResRelatedData
from main_pack.models.commerce.models import Resource,Res_category

@bp.route("/")
@bp.route("/commerce")
def commerce():
	resources = Resource.query.order_by(Resource.CreatedDate.desc())
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/commerce.html",
		resources=resources,**commonData,**resData)

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
	resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/cart.html",
		resources=resources,**commonData,**resData,title=gettext('Cart'))

@bp.route("/product")
def product_ol():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/product_ol.html",**commonData,title=gettext('Product'))

@bp.route("/account")
def account():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/account.html",**commonData,title=gettext('Account'))

@bp.route("/account_edit")
def account_edit():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/account_edit.html",**commonData,title=gettext('Account'))

#  pagiantions ########
@bp.route("/list_paginate")
def list_paginate():
	page = request.args.get('page',1,type=int)
	resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/list_paginate.html",
		resources=resources,**commonData,**resData,title=gettext('Category'),
		pagination_url='commerce.list_paginate')

@bp.route("/grid_paginate")
def grid_paginate():
	page = request.args.get('page',1,type=int)
	resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/grid_paginate.html",
		resources=resources,**commonData,**resData,title=gettext('Category'),
		pagination_url='commerce.grid_paginate')

@bp.route("/product/<int:resId>")
def product(resId):
	resource = Resource.query.get(resId)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/product.html",
		resource=resource,**commonData,**resData,title=gettext('Product'))

### sorting and search

@bp.route("/category_product/")
def category_product():
	catName = request.args.get('catName','futbolkalar')
	page = request.args.get('page',1,type=int)
	category = Res_category.query.filter_by(ResCatName=catName).first()
	resources = Resource.query.filter_by(ResCatId=category.ResCatId)\
		.order_by(Resource.CreatedDate.desc())\
		.paginate(per_page=20,page=page)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/grid_paginate.html",
		resources=resources,**commonData,**resData,title=gettext('Category'),
		pagination_url='commerce.category_product',catName=catName)

@bp.route("/search/<string:resName>/")
def ui_search(resName):
	resources=[]
	allResources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)
	for resource in allResources:
		if(resource.ResName[0:len(resName)]==resName):
			resources.append(resource)
	commonData = commonUsedData()
	resData = realResRelatedData()
	return render_template ("commerce/main/commerce/searchNavigation.html",
		resources=resources,**commonData,**resData)



# @bp.route("/rest_grid")
# def rest_grid():
# 	if request=='POST':
# 		req = request.get_json()
# 		ColorId = req.get('colorId')
# 		BrandId = req.get('brandId')
# 		SizeId = req.get('sizeId')
# 		ResCatId = req.get('resCatId')
# 		page = req.get('page',1)
# 		resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
# 			.filter(Resource.ResCatId==resCatId)\
# 			.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
# 		commonData = commonUsedData()
# 		resData = realResRelatedData()
# 		return jsonify({'resources':resources})

# 	else:
# 		# page = request.args.get('page',1,type=int)
# 		resources = Resource.query.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
# 			.order_by(Resource.CreatedDate.desc()).paginate(per_page=20,page=page)
# 		commonData = commonUsedData()
# 		resData = realResRelatedData()
# 		return render_template ("commerce/main/commerce/rest_grid.html",
# 			resources=resources,**commonData,**resData,title=gettext('Category'))
