from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.users import bp
from main_pack.commerce.users.utils import commonUsedData

from main_pack.models.base.models import Rp_acc



@bp.route("/orders")
@login_required
def orders():
	commonData = commonUsedData()
	return render_template ("commerce/main/users/orders.html",**commonData,title=gettext('Orders'))


@bp.route("/orders_list")
def orders_list():
	commonData = commonUsedData()
	return render_template ("commerce/main/users/orders_list.html",**commonData,title=gettext('Orders'))

