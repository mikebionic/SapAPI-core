from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.commerce.commerce.utils import (commonUsedData,realResRelatedData,
	UiResourcesList,UiCategoriesList,slidersData,UiResLimitedList)
from main_pack.models.commerce.models import Resource,Res_category

@bp.route("/")
@bp.route("/commerce")
def commerce():
	res = UiResLimitedList(100)
	sl_images = slidersData()
	# commonData = commonUsedData()
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/commerce.html",
		**res,**categoriesData,**sl_images)

@bp.route("/collection")
def collection():
	categoriesData = UiCategoriesList()
	# commonData = commonUsedData()
	return render_template ("commerce/main/commerce/collection.html",**categoriesData,title=gettext('Collection'))

@bp.route("/about")
def about():
	categoriesData = UiCategoriesList()
	# commonData = commonUsedData()
	return render_template ("commerce/main/commerce/about.html",**categoriesData,title=gettext('About us'))

@bp.route("/contact")
def contact():
	categoriesData = UiCategoriesList()
	# commonData = commonUsedData()
	return render_template ("commerce/main/commerce/contact.html",**categoriesData,title=gettext('Contact'))

@bp.route("/cart")
def cart():
	categoriesData = UiCategoriesList()
	# commonData = commonUsedData()
	return render_template ("commerce/main/commerce/cart.html",
		**categoriesData,title=gettext('Cart'))

### sorting and search

# @bp.route("/category_product/")
# def category_product():
# 	catName = request.args.get('catName','futbolkalar')
# 	page = request.args.get('page',1,type=int)
# 	category = Res_category.query.filter_by(ResCatName=catName).first()
# 	resources = Resource.query.filter_by(ResCatId=category.ResCatId)\
# 		.order_by(Resource.CreatedDate.desc())\
# 		.paginate(per_page=20,page=page)
	# commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	return render_template ("commerce/main/commerce/v_grid.html",
# 		resources=resources,**resData,title=gettext('Category'),
# 		pagination_url='commerce.category_product',catName=catName)
