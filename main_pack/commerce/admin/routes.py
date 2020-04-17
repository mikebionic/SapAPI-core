from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp

@bp.route("/admin/dashboard")
def dashboard_commerce():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/navbar")
def navbar_commerce():
	return render_template ("commerce/admin/navbar.html",title=gettext('Navbar'))

@bp.route("/admin/picture")
def picture_commerce():
	return render_template ("commerce/admin/picture.html",title=gettext('Picture'))

@bp.route("/admin/product_table")
def product_table_commerce():
	return render_template ("commerce/admin/product_table.html",title=gettext('Product table'))

@bp.route("/admin/single_product")
def single_product_commerce():
	return render_template ("commerce/admin/single_product.html",title=gettext('Single product'))
