from flask import render_template, url_for, jsonify
from flask_login import current_user, login_required

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import db, gettext

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo, apiFeaturedResCat_Resources
from main_pack.commerce.commerce.utils import (
	slidersData,
	UiCategoriesList,
	UiBrandsList,
	send_email_to_company)

from main_pack.commerce.commerce.forms import SendEmailToCompanyForm
# / Resource and view /


@bp.route("/")
@bp.route(Config.COMMERCE_HOME_PAGE)
def commerce():
	latest_resources = apiResourceInfo(showLatest = True)
	# rated_resources = apiResourceInfo(showRated = True)
	featured_categories = apiFeaturedResCat_Resources()
	brands = UiBrandsList()
	# "Rated_resources": rated_resources['data'],
	res = {
		"Latest_resources": latest_resources['data'],
		"Featured_categories": featured_categories['data'],
		"Brands": brands['data']
	}
	sliders = slidersData()
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/commerce.html",
		**res,
		**categoriesData,
		**sliders,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_HOME_PAGE_TITLE))


@bp.route(Config.COMMERCE_COLLECTION_VIEW)
def collection():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/collection.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_COLLECTION_VIEW_TITLE))


@bp.route(Config.COMMERCE_ABOUT_PAGE)
def about():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/about.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_ABOUT_PAGE_TITLE))


@bp.route(Config.COMMERCE_CONTACTS_PAGE, methods=['GET', 'POST'])
def contact():
	categoriesData = UiCategoriesList()
	form = SendEmailToCompanyForm()
	if form.validate_on_submit():
		email_data = {
			"FirstName": form.FirstName.data,
			"LastName": form.LastName.data,
			"Email": form.Email.data,
			"Phone": form.Phone.data,
			"Message": form.Message.data
		}

		message	= f'''Message from user.
		Email: {email_data["Email"]},
		First name: {email_data["FirstName"]},
		Last name: {email_data["LastName"]},
		Phone: {email_data["Phone"]},
		Message: {email_data["Message"]}
		'''
		send_email_to_company(message)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/contact.html",
		**categoriesData,
		form = form,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_CONTACTS_PAGE_TITLE))


@bp.route(Config.COMMERCE_CART_VIEW)
def cart():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cart.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_CART_VIEW_TITLE))


@bp.route(Config.COMMERCE_BRAND_PAGE)
def brand():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/brand.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_BRAND_PAGE_TITLE))




