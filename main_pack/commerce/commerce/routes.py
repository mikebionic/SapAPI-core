from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import slidersData,UiCategoriesList
from main_pack.models.commerce.models import Resource,Res_category
# / Resource and view /

@bp.route("/")
@bp.route("/commerce")
def commerce():
	res = apiResourceInfo()
	sliders = slidersData()
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/commerce.html",
		**res,**categoriesData,**sliders)

@bp.route("/collection")
def collection():
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/collection.html",**categoriesData,title=gettext('Collection'))

@bp.route("/about")
def about():
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/about.html",**categoriesData,title=gettext('About us'))

@bp.route("/contact")
def contact():
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/contact.html",**categoriesData,title=gettext('Contact'))

@bp.route("/cart")
def cart():
	categoriesData = UiCategoriesList()
	return render_template ("commerce/main/commerce/cart.html",
		**categoriesData,title=gettext('Cart'))
