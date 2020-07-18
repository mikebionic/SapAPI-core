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
from main_pack.base.languageMethods import dataLangSelector
from main_pack.models.commerce.models import Res_category

import os
from main_pack.base.imageMethods import allowed_icon
from flask import current_app

from main_pack.commerce.admin.users_utils import UiRpAccData,UiUsersData
from main_pack.models.users.models import (Users,User_type,
																					Rp_acc,Rp_acc_type,Rp_acc_status)

@bp.route("/admin")
@bp.route("/admin/dashboard")
@login_required
@ui_admin_required()
def dashboard():
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

@bp.route("/admin/login")
def login():
	return render_template ("commerce/admin/login.html",title=gettext('Login'))

###### categories management and shop info #######
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
		try:
			folder_icons = os.listdir(os.path.join(full_icons_path,folder))
			icons = []
			for icon in folder_icons:
				if allowed_icon(icon):
					iconInfo = {
						'url':url_for('commerce_api.get_icon',category=folder,file_name=icon),
						'icon_name':icon,
						'category':folder
					}
					icons.append(iconInfo)
			category_icons[folder]=icons
		except:
			print("Err: not a folder")

	data['category_icons']=category_icons
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()

	categoriesList = [category.to_json_api() for category in categories]
	data['categories'] = categoriesList if categoriesList else []
	return render_template ("commerce/admin/category_table.html",
		**data,title=gettext('Category table'))
###################################

@bp.route("/admin/product_table")
@login_required
@ui_admin_required()
def product_table():
	resData=UiResourcesList()
	print(resData)
	return render_template ("commerce/admin/product_table.html",**resData,
		title=gettext('Product table'))


@bp.route("/admin/admin_table")
@login_required
@ui_admin_required()
def admin_table():
	return render_template ("commerce/admin/admin_table.html",title=gettext('Admin table'))

##### customers table and customers information ######
@bp.route("/admin/customers_table")
@login_required
@ui_admin_required()
def customers_table():
	data = UiRpAccData()

	rp_acc_statuses = Rp_acc_status.query\
		.filter(Rp_acc_status.GCRecord=='' or Rp_acc_status.GCRecord==None).all()
	rp_acc_statuses_list = []
	for rp_acc_status in rp_acc_statuses:
		rp_acc_statuses_list.append(dataLangSelector(rp_acc_status.to_json_api()))
	data['rp_acc_statuses'] = rp_acc_statuses_list

	rp_acc_types = Rp_acc_type.query\
		.filter(Rp_acc_type.GCRecord=='' or Rp_acc_type.GCRecord==None).all()
	rp_acc_types_list = []
	for rp_acc_type in rp_acc_types:
		rp_acc_types_list.append(dataLangSelector(rp_acc_type.to_json_api()))
	data['rp_acc_types'] = rp_acc_types_list

	return render_template ("commerce/admin/customers_table.html",**data,title=gettext('Customers'))

@bp.route("/admin/customer_details/<RpAccId>")
@login_required
@ui_admin_required()
def customer_details(RpAccId):
	try:
		data = UiRpAccData([{'RpAccId':RpAccId}])
		data['rp_acc']=data['rp_accs'][0]
		
		rp_acc_statuses = Rp_acc_status.query\
			.filter(Rp_acc_status.GCRecord=='' or Rp_acc_status.GCRecord==None).all()
		rp_acc_statuses_list = []
		for rp_acc_status in rp_acc_statuses:
			rp_acc_statuses_list.append(dataLangSelector(rp_acc_status.to_json_api()))
		data['rp_acc_statuses'] = rp_acc_statuses_list

		rp_acc_types = Rp_acc_type.query\
			.filter(Rp_acc_type.GCRecord=='' or Rp_acc_type.GCRecord==None).all()
		rp_acc_types_list = []
		for rp_acc_type in rp_acc_types:
			rp_acc_types_list.append(dataLangSelector(rp_acc_type.to_json_api()))
		data['rp_acc_types'] = rp_acc_types_list

		orderInvoices = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),
				Order_inv.RpAccId==RpAccId)\
			.order_by(Order_inv.CreatedDate.desc()).all()
		orders_list = []
		for orderInv in orderInvoices:
			order = {}
			order['OInvId'] = orderInv.OInvId
			orders_list.append(order)
		orderInvRes = UiOInvData(orders_list)
	except:
		return redirect(url_for('commerce_admin.customers_table'))
	return render_template ("commerce/admin/customer_details.html",
		**data,**orderInvRes,title=gettext('Customer details'))

@bp.route("/admin/register_customer")
@login_required
@ui_admin_required()
def register_customer():
	return render_template ("commerce/admin/register_customer.html",title=gettext('Register'))

@bp.route("/admin/customer_details/<RpAccId>/remove")
@login_required
@ui_admin_required()
def remove_customer(RpAccId):
	try:
		rp_acc = Rp_acc.query\
			.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
				Rp_acc.RpAccId==RpAccId).first()
		rp_acc.GCRecord=1

		user = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
				Users.RpAccId==RpAccId).first()
		if user:
			user.GCRecord=1
		db.session.commit()
		flash('{} '.format(rp_acc.RpAccName)+lazy_gettext('successfully deleted'),'success')
	except:
		flash('Unknown error!','danger')
	return redirect(url_for('commerce_admin.customers_table'))

################################

###### users and user information #####
@bp.route("/admin/users_table")
@login_required
@ui_admin_required()
def users_table():
	data = UiUsersData()
	user_types = User_type.query\
		.filter(User_type.GCRecord=='' or User_type.GCRecord==None).all()
	user_types_list = []
	for user_type in user_types:
		user_types_list.append(dataLangSelector(user_type.to_json_api()))
	data['user_types'] = user_types_list

	return render_template ("commerce/admin/users_table.html",**data,title=gettext('Users'))

@bp.route("/admin/register_user")
@login_required
@ui_admin_required()
def register_user():
	return render_template ("commerce/admin/register_user.html",title=gettext('Register'))

@bp.route("/admin/user_details/<UId>/remove")
@login_required
@ui_admin_required()
def remove_user(UId):
	try:
		user = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
				Users.UId==UId).first()
		user.GCRecord=1
		db.session.commit()
		flash('{} '.format(user.UName)+lazy_gettext('successfully deleted'),'success')
	except:
		flash('Unknown error!','danger')
	return redirect(url_for('commerce_admin.users_table'))
#################################

###### orders and order information #######
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
	orderInvRes = UiOInvData(orders_list)

	return render_template ("commerce/admin/order_invoices.html",**orderInvRes,
		title=gettext('Order invoices'))

@bp.route("/admin/order_invoices/<OInvRegNo>",methods=['GET','POST'])
@login_required
@ui_admin_required()
def order_inv_lines(OInvRegNo):
	orderInvoice = Order_inv.query\
		.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),
								Order_inv.OInvRegNo==OInvRegNo).first()
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
	orderInvLineRes = UiOInvLineData(order_lines_list)
	inv_statuses = Inv_status.query\
		.filter(Inv_status.GCRecord=='' or Inv_status.GCRecord==None).all()
	invoice_statuses = []
	for inv_stat in inv_statuses:
		invoice_statuses.append(dataLangSelector(inv_stat.to_json_api()))
	InvoiceStatuses = {'inv_statuses':invoice_statuses}
	return render_template ("commerce/admin/order_inv_lines.html",
		**orderInvLineRes,**InvoiceStatuses,**orderInvRes,title=gettext('Order invoices'))
#########################################

@bp.route("/admin/add_product")
@login_required
@ui_admin_required()
def add_product():
	resData=resRelatedData()
	return render_template ("commerce/admin/add_product.html",**resData,title=gettext('Add product'))