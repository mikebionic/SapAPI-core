from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import prepare_data
from main_pack.commerce.commerce.utils import commonUsedData
from main_pack.commerce.admin.utils import resRelatedData

from main_pack.commerce.commerce.utils import UiResourcesList

from main_pack.commerce.users.routes import admin_required

@bp.route("/admin/dashboard")
@login_required
@admin_required()
def dashboard():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/navbar")
@login_required
@admin_required()
def navbar():
	# categoryData = UiCategoriesList()
	commonData = commonUsedData()
	return render_template ("commerce/admin/navbar.html",**commonData,title=gettext('Navbar'))

@bp.route("/admin/picture")
@login_required
@admin_required()
def picture():
	return render_template ("commerce/admin/picture.html",title=gettext('Picture'))

@bp.route("/admin/product_table")
@login_required
@admin_required()
def product_table():
	resData=UiResourcesList()
	print(resData)
	return render_template ("commerce/admin/product_table.html",**resData,
		title=gettext('Product table'))


@bp.route("/admin/order_invoices")
@login_required
@admin_required()
def order_invoices():

	return render_template ("commerce/admin/order_invoices.html",
		title=gettext('Order invoices'))

@bp.route("/admin/add_product")
@login_required
@admin_required()
def add_product():
	resData=resRelatedData()
	return render_template ("commerce/admin/add_product.html",**resData,title=gettext('Add product'))

@bp.route("/admin/orders")
def orders():
	resData=resRelatedData()
	return render_template ("commerce/admin/orders.html",**resData,title=gettext('Orders'))
