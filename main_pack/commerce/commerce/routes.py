from flask import render_template, flash, session
from flask_login import current_user, login_required

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import gettext
from main_pack.base import log_print

from main_pack.api.commerce.commerce_utils import apiResourceInfo, apiFeaturedResCat_Resources
from main_pack.commerce.commerce.utils import (
	slidersData,
	UiCategoriesList,
	UiBrandsList,
	send_email_to_company,
)

from main_pack.commerce.commerce.forms import SendEmailToCompanyForm
from main_pack.api.common import get_payment_methods


@bp.route("/")
@bp.route(Config.COMMERCE_HOME_PAGE)
def commerce():
	latest_resources = apiResourceInfo(showLatest = True)
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

	if Config.COMMERCE_SHOW_FEATURED_PRODUCTS:
		featured_resources = apiResourceInfo(
			order_by_visible_index = True,
			limit_by = 10,
		)
		res["Featured_products"] = featured_resources["data"]

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

@bp.route(Config.COMMERCE_RESOURCE_REQUEST_PAGE)
def resource_request():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/resource_request.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_ABOUT_PAGE_TITLE))



@bp.route(Config.COMMERCE_CONTACTS_PAGE, methods=['GET', 'POST'])
def contact():
	categoriesData = UiCategoriesList()
	form = SendEmailToCompanyForm()

	flashing_message = ("{}".format(gettext("Error occured, please try again.")))
	message_style = 'warning'
	extra_data = ''

	if form.validate_on_submit():
		email_data = {
			"FirstName": form.FirstName.data,
			"LastName": form.LastName.data,
			"Email": form.Email.data,
			"Phone": form.Phone.data,
			"Message": form.Message.data
		}

		if (current_user.is_authenticated and "model_type" in session):
			if session["model_type"] == "rp_acc":
				try:
					extra_data = f'''
					------
					Logged user
					Username: {current_user.RpAccUName}
					Full name: {current_user.RpAccName}
					Phone: {current_user.RpAccMobilePhoneNumber}
					Email: {current_user.RpAccEMail}
					'''
				except Exception as ex:
					log_print(f"Email to company extra user data Exception: {ex}", "warning")

		message	= f'''Message from user.
		Email: {email_data["Email"]},
		First name: {email_data["FirstName"]},
		Last name: {email_data["LastName"]},
		Phone: {email_data["Phone"]},
		Message: {email_data["Message"]}
		{extra_data}
		'''
		state = send_email_to_company(message)
		if state:
			flashing_message = ("{} {}!".format(gettext("Message"), gettext("successfully sent")))
			message_style = 'success'

		flash(flashing_message, message_style)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/contact.html",
		**categoriesData,
		form = form,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_CONTACTS_PAGE_TITLE))


@bp.route(Config.COMMERCE_CART_VIEW)
def cart():
	categoriesData = UiCategoriesList()
	payment_methods = get_payment_methods()

	if "currency_code" not in session:
		session["currency_code"] = "TMT"

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/cart.html",
		**categoriesData,
		payment_methods = payment_methods,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_CART_VIEW_TITLE))


@bp.route("/payment-validation/")
@bp.route("/payment-validation/<OrderId>")
@login_required
def render_payment_validation_view(OrderId = None):
	categoriesData = UiCategoriesList()

	if "currency_code" not in session:
		session["currency_code"] = "TMT"

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/validate_payment.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_CART_VIEW_TITLE))


@bp.route(Config.COMMERCE_BRANDS_PAGE)
def brands():
	categoriesData = UiCategoriesList()
	brands = UiBrandsList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/brands.html",
		**categoriesData,
		brands = brands["data"],
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_BRANDS_PAGE_TITLE))

		
@bp.route(Config.COMMERCE_ORDER_BOOK_PAGE)
def order_book():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/order_book.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_ORDER_BOOK_PAGE_TITLE))


@bp.route(Config.COMMERCE_NEWS_PAGE)
def news():
	categoriesData = UiCategoriesList()

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/commerce/news.html",
		**categoriesData,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_NEWS_PAGE_TITLE))