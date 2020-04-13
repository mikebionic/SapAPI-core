from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db, babel
from main_pack.commerce.commerce import bp

@bp.route("/")
def commerce():
	return render_template ("commerce/main/commerce/commerce.html")

@bp.route("/collection")
@login_required
def collection():
	return render_template ("commerce/main/commerce/collection.html",title='Collection')

@bp.route("/about")
def about():
	return render_template ("commerce/main/commerce/about.html",title='About us')

@bp.route("/contact")
def contact():
	return render_template ("commerce/main/commerce/contact.html",title='Contact')

@bp.route("/cart")
def cart():
	return render_template ("commerce/main/commerce/cart.html",title='Cart')

@bp.route("/product")
def product():
	return render_template ("commerce/main/commerce/product.html",title='Product')

@bp.route("/category_list")
def category_list():
	return render_template ("commerce/main/commerce/category_list.html",title='Category')

@bp.route("/category_grid")
def category_grid():
	return render_template ("commerce/main/commerce/category_grid.html",title='Category')
