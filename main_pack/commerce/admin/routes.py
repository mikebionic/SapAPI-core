from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import prepare_data,resRelatedData
from main_pack.commerce.commerce.utils import commonUsedData,UiResourcesList

from main_pack.commerce.users.routes import ui_admin_required

from main_pack.models.commerce.models import (Inv_line,Inv_line_det,Inv_line_det_type,
	Inv_status,Inv_type,Invoice,Order_inv,Order_inv_line,Order_inv_type)
from main_pack.commerce.commerce.order_utils import UiOInvData,UiOInvLineData
from sqlalchemy import and_

from main_pack.commerce.commerce.order_utils import invStatusesSelectData
from main_pack.models.commerce.models import Res_category

import os
from flask import current_app

@bp.route("/admin")
@bp.route("/admin/dashboard")
@login_required
@ui_admin_required()
def dashboard():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/navbar")
@login_required
@ui_admin_required()
def navbar():
	icons_path = os.path.join("static","commerce","icons","categories")
	full_icons_path = os.path.join(current_app.root_path,icons_path)
	folders = os.listdir(full_icons_path)
	category_icons = {} 
	for folder in folders:
		folder_icons = os.listdir(os.path.join(full_icons_path,folder))
		icons = []
		for icon in folder_icons:
			iconInfo = {
				'url':url_for('commerce_api.get_icon',category=folder,file_name=icon),
				'icon_name':icon,
				'category':folder
			}
			icons.append(iconInfo)
		category_icons[folder]=icons

	commonData = commonUsedData()
	return render_template ("commerce/admin/navbar.html",**commonData,category_icons=category_icons,
		title=gettext('Navbar'))

@bp.route("/admin/category_table")
@login_required
@ui_admin_required()
def category_table():
	data = {}
	icons_path = os.path.join("static","commerce","icons","categories")
	full_icons_path = os.path.join(current_app.root_path,icons_path)
	folders = os.listdir(full_icons_path)
	category_icons = {}
	for folder in folders:
		folder_icons = os.listdir(os.path.join(full_icons_path,folder))
		icons = []
		for icon in folder_icons:
			iconInfo = {
				'url':url_for('commerce_api.get_icon',category=folder,file_name=icon),
				'icon_name':icon,
				'category':folder
			}
			icons.append(iconInfo)
		category_icons[folder]=icons

	data['category_icons']=category_icons
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()

	categoriesList = [category.to_json_api() for category in categories]
	data['categories'] = categoriesList if categoriesList else []
	return render_template ("commerce/admin/category_table.html",
		**data,title=gettext('Category table'))

@bp.route("/admin/picture")
@login_required
@ui_admin_required()
def picture():
	return render_template ("commerce/admin/picture.html",title=gettext('Picture'))

@bp.route("/admin/product_table")
@login_required
@ui_admin_required()
def product_table():
	resData=UiResourcesList()
	print(resData)
	return render_template ("commerce/admin/product_table.html",**resData,
		title=gettext('Product table'))

@bp.route("/admin/order_invoices")
@login_required
@ui_admin_required()
def order_invoices():
	orderInvoices = Order_inv.query\
		.filter(Order_inv.GCRecord=='' or Order_inv.GCRecord==None)\
		.order_by(Order_inv.CreatedDate.desc()).all()
	
	orders_list = []
	for orderInv in orderInvoices:
		order = {}
		order['OInvId'] = orderInv.OInvId
		orders_list.append(order)
	res = UiOInvData(orders_list)

	return render_template ("commerce/admin/order_invoices.html",**res,
		title=gettext('Order invoices'))

@bp.route("/admin/order_invoices/<OInvRegNo>",methods=['GET','POST'])
@login_required
@ui_admin_required()
def order_inv_lines(OInvRegNo):
	orderInvoice = Order_inv.query\
		.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),
								Order_inv.OInvRegNo==OInvRegNo)\
		.first()
	orderInvRes = UiOInvData([{'OInvId':orderInvoice.OInvId}])
	
	orderInvLines = Order_inv_line.query\
		.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),
									Order_inv_line.OInvId==orderInvoice.OInvId)\
		.order_by(Order_inv_line.CreatedDate.desc()).all()

	order_lines_list = []
	for orderInvLine in orderInvLines:
		order_inv_line = {}
		order_inv_line['OInvLineId'] = orderInvLine.OInvLineId
		order_lines_list.append(order_inv_line)
	res = UiOInvLineData(order_lines_list)

	return render_template ("commerce/admin/order_inv_lines.html",**res,
		**orderInvRes,title=gettext('Order invoices'))

@bp.route("/admin/add_product")
@login_required
@ui_admin_required()
def add_product():
	resData=resRelatedData()
	return render_template ("commerce/admin/add_product.html",**resData,title=gettext('Add product'))

@bp.route("/admin/orders")
def orders():
	resData=resRelatedData()
	return render_template ("commerce/admin/orders.html",**resData,title=gettext('Orders'))
