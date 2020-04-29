from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

from main_pack.models.base.models import Res_category,Company

def commonUsedData():
	commonData = {}
	subcategories = []
	subcategory_children = []
	company = Company.query.get(1)
	categories = Res_category.query.filter_by(ResOwnerCatId=0)
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				subcategories.append(category)
			else:
				subcategory_children.append(category)

	commonData.update({
		"categories":categories,
		"subcategories":subcategories,
		"subcategory_children":subcategory_children,
		"company":company
		})
	return commonData

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
def product():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/product.html",**commonData,title=gettext('Product'))

@bp.route("/category_list")
def category_list():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/category_list.html",**commonData,title=gettext('Category'))

@bp.route("/category_grid")
def category_grid():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/category_grid.html",**commonData,title=gettext('Category'))
