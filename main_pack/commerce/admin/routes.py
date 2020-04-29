from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import prepare_data
from main_pack.models.base.models import Res_category,Company

@bp.route("/admin/dashboard")
def dashboard():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/navbar")
def navbar():
	baseTemplate = {}
	subcategories = []
	subcategory_children = []
	company = Company.query.get(1)
	categories = Res_category.query.filter_by(ResOwnerCatId=0)
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				subcategories.append(category)
			else:
				subcategory_children.append(category)

	baseTemplate.update({
		"categories":categories,
		"subcategories":subcategories,
		"subcategory_children":subcategory_children,
		"company":company
		})
	return render_template ("commerce/admin/navbar.html", **baseTemplate,title=gettext('Navbar'))


@bp.route("/admin/picture")
def picture():
	return render_template ("commerce/admin/picture.html",title=gettext('Picture'))

@bp.route("/admin/product_table")
def product_table():
	return render_template ("commerce/admin/product_table.html",title=gettext('Product table'))

@bp.route("/admin/single_product")
def single_product():
	return render_template ("commerce/admin/single_product.html",title=gettext('Single product'))
