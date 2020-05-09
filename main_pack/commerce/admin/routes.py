from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import prepare_data
from main_pack.commerce.commerce.utils import commonUsedData
from main_pack.commerce.admin.utils import resRelatedData

@bp.route("/admin/dashboard")
def dashboard():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/navbar")
def navbar():
	commonData = commonUsedData()
	return render_template ("commerce/admin/navbar.html",**commonData,title=gettext('Navbar'))

@bp.route("/admin/picture")
def picture():
	return render_template ("commerce/admin/picture.html",title=gettext('Picture'))

@bp.route("/admin/product_table")
def product_table():
	return render_template ("commerce/admin/product_table.html",title=gettext('Product table'))

@bp.route("/admin/single_product")
def single_product():
	return render_template ("commerce/admin/single_product.html",title=gettext('Single product'))

@bp.route("/admin/add_product")
def add_product():
	resData=resRelatedData()
	return render_template ("commerce/admin/add_product.html",**resData,title=gettext('Single product'))
