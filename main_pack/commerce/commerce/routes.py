from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack.config import Config
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo,apiFeaturedResCat_Resources
from main_pack.commerce.commerce.utils import slidersData,UiCategoriesList
# from main_pack.models.commerce.models import Resource
# / Resource and view /

@bp.route("/")
@bp.route(Config.COMMERCE_HOME_PAGE)
def commerce():
	latest_resources = apiResourceInfo(showLatest = True)
	rated_resources = apiResourceInfo(showRated = True)
	featured_categories = apiFeaturedResCat_Resources()
	res = {
		"Latest_resources": latest_resources['data'],
		"Rated_resources": rated_resources['data'],
		"Featured_categories": featured_categories['data']
	}
	sliders = slidersData()
	categoriesData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/commerce.html",
		**res,**categoriesData,**sliders,title=gettext(Config.COMMERCE_HOME_PAGE_TITLE))

@bp.route(Config.COMMERCE_COLLECTION_VIEW)
def collection():
	categoriesData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/collection.html",
		**categoriesData,title=gettext(Config.COMMERCE_COLLECTION_VIEW_TITLE))

@bp.route(Config.COMMERCE_ABOUT_PAGE)
def about():
	categoriesData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/about.html",
		**categoriesData,title=gettext(Config.COMMERCE_ABOUT_PAGE_TITLE))

@bp.route(Config.COMMERCE_CONTACTS_PAGE)
def contact():
	categoriesData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/contact.html",
		**categoriesData,title=gettext(Config.COMMERCE_CONTACTS_PAGE_TITLE))

@bp.route(Config.COMMERCE_CART_VIEW)
def cart():
	categoriesData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"commerce/cart.html",
		**categoriesData,title=gettext(Config.COMMERCE_CART_VIEW_TITLE))
