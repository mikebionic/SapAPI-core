from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack.config import Config
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import slidersData,UiCategoriesList
from main_pack.models.commerce.models import Resource,Res_category
# / Resource and view /

@bp.route("/")
@bp.route(Config.COMMERCE_HOME_PAGE)
def commerce():
	latest_resources = apiResourceInfo(showLatest = True)
	rated_resources = apiResourceInfo(showRated = True)
	featured_resources = Resource.query\
		.filter_by(GCRecord = None)\
		.outerjoin(Res_category, Res_category.ResCatId == Resource.ResCatId)\
		.filter(Res_category.GCRecord == None)\
		.filter(Res_category.IsMain == True)\
		.order_by(Resource.CreatedDate.desc())\
		.limit(50)\
		.all()
	resource_models = [resource for resource in featured_resources if featured_resources]
	featured_resources = apiResourceInfo(resource_models = resource_models)

	featured_categories = Res_category.query\
		.filter_by(GCRecord = None)\
		.filter(Res_category.IsMain == True)\
		.all()
	Featured_categories_list = []
	if featured_categories:
		for category in featured_categories:
			featured_category = category.to_json_api()
			resources_list = []
			for resource in featured_resources['data']:
				if resource['ResCatId'] == category.ResCatId:
					resources_list.append(resource)
			featured_category['Resources'] = resources_list
			Featured_categories_list.append(featured_category)

	res = {
		"Latest_resources": latest_resources['data'],
		"Rated_resources": rated_resources['data'],
		"Featured_categories": Featured_categories_list,
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
