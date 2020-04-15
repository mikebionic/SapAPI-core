from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

@bp.route("/")
def commerce():
	return render_template ("commerce/main/commerce/commerce.html")

@bp.route("/collection")
def collection_commerce():
	return render_template ("commerce/main/commerce/collection.html",title=gettext('Collection'))

@bp.route("/about")
def about_commerce():
	return render_template ("commerce/main/commerce/about.html",title=gettext('About us'))

@bp.route("/contact")
def contact_commerce():
	return render_template ("commerce/main/commerce/contact.html",title=gettext('Contact'))

@bp.route("/cart")
def cart_commerce():
	return render_template ("commerce/main/commerce/cart.html",title=gettext('Cart'))

@bp.route("/product")
def product_commerce():
	return render_template ("commerce/main/commerce/product.html",title=gettext('Product'))

@bp.route("/category_list")
def category_list_commerce():
	return render_template ("commerce/main/commerce/category_list.html",title=gettext('Category'))

@bp.route("/category_grid")
def category_grid_commerce():
	return render_template ("commerce/main/commerce/category_grid.html",title=gettext('Category'))
