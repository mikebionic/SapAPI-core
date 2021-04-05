from flask import render_template, url_for, session, redirect
from flask_login import current_user, login_required
from sqlalchemy import and_

from . import bp, url_prefix
from main_pack import db, gettext, lazy_gettext
from main_pack.config import Config
from main_pack.commerce.commerce.utils import UiCategoriesList
# change this for something else

from main_pack.models import (
	Inv_line,
	Inv_line_det,
	Inv_line_det_type,
	Inv_status,
	Inv_type,
	Invoice,
	Order_inv,
	Order_inv_line,
	Order_inv_type)

from main_pack.commerce.commerce.order_utils import UiOInvData, UiOInvLineData


@bp.route(Config.COMMERCE_ORDERS_PAGE)
@login_required
def orders():
	orderInvoices = Order_inv.query\
		.filter_by(GCRecord = None, RpAccId = current_user.RpAccId)\
		.order_by(Order_inv.CreatedDate.desc())\
		.all()
	
	orders_list = []
	for orderInv in orderInvoices:
		order = {}
		order['OInvId'] = orderInv.OInvId
		orders_list.append(order)

	res = UiOInvData(orders_list)

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/orders.html",
		**categoryData,
		**res,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_ORDERS_PAGE_TITLE))


@bp.route(Config.COMMERCE_ORDERS_PAGE+"/<OInvRegNo>")
@login_required
def order_lines(OInvRegNo):
	orderInvoice = Order_inv.query\
		.filter_by(GCRecord = None, OInvRegNo = OInvRegNo)\
		.first()

	if orderInvoice.RpAccId == current_user.RpAccId:
		orderInvRes = UiOInvData([{'OInvId':orderInvoice.OInvId}])
		
		orderInvLines = Order_inv_line.query\
			.filter_by(GCRecord = None, OInvId = orderInvoice.OInvId)\
			.order_by(Order_inv_line.CreatedDate.desc())\
			.all()

		order_lines_list = []
		for orderInvLine in orderInvLines:
			order_inv_line = {}
			order_inv_line['OInvLineId'] = orderInvLine.OInvLineId
			order_lines_list.append(order_inv_line)
		res = UiOInvLineData(order_lines_list)
		
		categoryData = UiCategoriesList()
		return render_template(
			f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/order_lines.html",
			**categoryData,
			**res,
			**orderInvRes,
			url_prefix = url_prefix,
			title = gettext(Config.COMMERCE_ORDERS_PAGE_TITLE))
	
	else:
		return redirect(url_for('commerce_users.orders'))
