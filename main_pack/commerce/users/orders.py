from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.users import bp
from main_pack.commerce.commerce.utils import UiCategoriesList
# change this for something else

@bp.route("/orders")
@login_required
def orders():
	
	categoryData = UiCategoriesList()
	return render_template ("commerce/main/users/orders.html",**categoryData,title=gettext('Orders'))


@bp.route("/orders_list")
def orders_list():
	categoryData = UiCategoriesList()
	return render_template ("commerce/main/users/orders_list.html",**categoryData,title=gettext('Orders'))

