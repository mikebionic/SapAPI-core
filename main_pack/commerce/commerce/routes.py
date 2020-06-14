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

### sorting and search

# @bp.route("/category_product/")
# def category_product():
# 	catName = request.args.get('catName','futbolkalar')
# 	page = request.args.get('page',1,type=int)
# 	category = Res_category.query.filter_by(ResCatName=catName).first()
# 	resources = Resource.query.filter_by(ResCatId=category.ResCatId)\
# 		.order_by(Resource.CreatedDate.desc())\
# 		.paginate(per_page=20,page=page)
# 	commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	return render_template ("commerce/main/commerce/v_grid.html",
# 		resources=resources,**commonData,**resData,title=gettext('Category'),
# 		pagination_url='commerce.category_product',catName=catName)
