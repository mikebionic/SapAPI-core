from flask import render_template,url_for,session,flash,redirect,request,Response,abort
from main_pack.commerce.admin import bp
import os
from flask import current_app
from main_pack.config import Config

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.languageMethods import dataLangSelector
from sqlalchemy import and_
# / useful methods /

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import commonUsedData
from main_pack.commerce.admin.utils import resRelatedData
# / Resource and view /

# Invoices
from main_pack.models.commerce.models import (Inv_line,Inv_line_det,Inv_line_det_type,
	Inv_status,Inv_type,Invoice,Order_inv,Order_inv_line,Order_inv_type)
from main_pack.commerce.commerce.order_utils import UiOInvData,UiOInvLineData
from main_pack.models.commerce.models import Res_category
# / Invoices /

# users and customers
from main_pack.models.users.models import (Users,User_type,
																					Rp_acc,Rp_acc_type,Rp_acc_status)
from main_pack.commerce.admin.users_utils import UiRpAccData,UiUsersData
from main_pack.commerce.admin.forms import UserRegistrationForm,CustomerRegistrationForm
# / users and customers /

# RegNo
from main_pack.key_generator.utils import makeRegNo,generate,validate
from datetime import datetime,timezone
# / RegNo /

# Image operations
from main_pack.models.base.models import Image
from main_pack.base.imageMethods import save_image
from main_pack.base.imageMethods import allowed_icon
# / Image operations /


@bp.route('/admin/language/<language>')
def set_language(language=None):
	session['language'] = language
	return redirect(url_for('commerce_admin.dashboard'))

@bp.route("/admin")
@bp.route("/admin/dashboard")
@login_required
@ui_admin_required()
def dashboard():
	print(current_user.UName)
	return render_template ("commerce/admin/dashboard.html",title=gettext('Dashboard'))

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
		except Exception as ex:
			print(ex)
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
	resData=apiResourceInfo(isInactive=True,fullInfo=True)
	return render_template ("commerce/admin/product_table.html",**resData,
		title=gettext('Product table'))

def rp_acc_types():
	rp_acc_types = Rp_acc_type.query\
			.filter(Rp_acc_type.GCRecord=='' or Rp_acc_type.GCRecord==None).all()
	rp_acc_types_list = []
	for rp_acc_type in rp_acc_types:
		rp_acc_types_list.append(dataLangSelector(rp_acc_type.to_json_api()))
	return rp_acc_types_list

def rp_acc_statuses():
	rp_acc_statuses = Rp_acc_status.query\
		.filter(Rp_acc_status.GCRecord=='' or Rp_acc_status.GCRecord==None).all()
	rp_acc_statuses_list = []
	for rp_acc_status in rp_acc_statuses:
		rp_acc_statuses_list.append(dataLangSelector(rp_acc_status.to_json_api()))
	return rp_acc_statuses_list

def user_types():
	user_types = User_type.query\
		.filter(User_type.GCRecord=='' or User_type.GCRecord==None).all()
	user_types_list = []
	for user_type in user_types:
		user_types_list.append(dataLangSelector(user_type.to_json_api()))
	return user_types_list

##### customers table and customers information ######
@bp.route("/admin/customers_table")
@login_required
@ui_admin_required()
def customers_table():
	data = UiRpAccData()
	data['rp_acc_statuses'] = rp_acc_statuses()
	data['rp_acc_types'] = rp_acc_types()
	return render_template ("commerce/admin/customers_table.html",**data,title=gettext('Customers'))

@bp.route("/admin/customer_details/<RpAccRegNo>")
@login_required
@ui_admin_required()
def customer_details(RpAccRegNo):
	try:
		rp_acc = Rp_acc.query\
			.filter(Rp_acc.RpAccRegNo==RpAccRegNo).first()
		RpAccId = rp_acc.RpAccId
		data = UiRpAccData([{'RpAccId':RpAccId}],deleted=True)
		data['rp_acc']=data['rp_accs'][0]

		data['rp_acc_statuses'] = rp_acc_statuses()
		data['rp_acc_types'] = rp_acc_types()

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
	except Exception as ex:
		print(ex)
		return redirect(url_for('commerce_admin.customers_table'))
	return render_template ("commerce/admin/customer_details.html",
		**data,**orderInvRes,title=gettext('Customer details'))

@bp.route("/admin/register_customer",methods=['GET','POST'])
@login_required
@ui_admin_required()
def register_customer():
	form = CustomerRegistrationForm()

	customer_types_list = rp_acc_types()
	customerTypeChoices=[]
	for customer_type in customer_types_list:
		obj=(customer_type['RpAccTypeId'],customer_type['RpAccTypeName'])
		customerTypeChoices.append(obj)
	form.customer_type.choices = customerTypeChoices

	vendor_users = Users.query\
		.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
			Users.RpAccId==None).all()
	vendorUserChoices=[]
	for vendor_user in vendor_users:
		obj=(vendor_user.UId,vendor_user.UName)
		vendorUserChoices.append(obj)
	form.vendor_user.choices = vendorUserChoices

	if form.validate_on_submit():
		try:
			username = form.username.data
			email = form.email.data
			full_name = form.full_name.data
			UShortName = (username[0]+username[-1]).upper()
			if Config.HASHED_PASSWORDS == True:
				password = bcrypt.generate_password_hash(form.password.data).decode() 
			else:
				password = form.password.data
			user = Users(
				UName=username,
				UEmail=email,
				UShortName=UShortName,
				UPass=password,
				UFullName=full_name,
				UTypeId=5)

			# get the regNum for RpAccount registration
			try:
				vendor = Users.query.get(form.vendor_user.data)
				if vendor.UShortName:
					reg_num = generate(UId=vendor.UId,prefixType='rp_code')
					regNo = makeRegNo(vendor.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
				else:
					reg_num = generate(UId=user.UId,prefixType='rp_code')
					regNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			except Exception as ex:
				print(ex)
				regNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())

			rp_acc = Rp_acc(
				RpAccUName=username,
				RpAccUPass=password,
				RpAccName=full_name,
				RpAccEMail=email,
				RpAccRegNo=regNo,
				RpAccTypeId=form.customer_type.data,
				RpAccAddress=form.address.data,
				RpAccMobilePhoneNumber=form.mobilePhone.data,
				RpAccHomePhoneNumber=form.homePhone.data,
				RpAccZipCode=form.zipCode.data,
				UId=form.vendor_user.data
				)
			db.session.add(rp_acc)
			db.session.commit()

			# assign the RpAccId to a User model
			user.RpAccId = rp_acc.RpAccId
			db.session.add(user)

			if form.picture.data:
				imageFile = save_image(imageForm=form.picture.data,module=os.path.join("uploads","commerce","Rp_acc"),id=rp_acc.RpAccId)
				lastImage = Image.query.order_by(Image.ImgId.desc()).first()
				ImgId = lastImage.ImgId+1
				image = Image(ImgId=ImgId,FileName=imageFile['FileName'],FilePath=imageFile['FilePath'],RpAccId=rp_acc.RpAccId)
				db.session.add(image)

			db.session.commit()

			flash('{} '.format(username)+lazy_gettext('successfully saved'),'success')
			return redirect(url_for('commerce_admin.customers_table'))
		except Exception as ex:
			print(ex)
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_admin.register_customer'))
	return render_template ("commerce/admin/register_customer.html",
		form=form,title=gettext('Register'))

################################

###### users and user information #####
@bp.route("/admin/users_table")
@login_required
@ui_admin_required()
def users_table():
	data = UiUsersData()
	data['user_types'] = user_types()
	return render_template ("commerce/admin/users_table.html",**data,title=gettext('Users'))

@bp.route("/admin/user_details/<UId>")
@login_required
@ui_admin_required()
def user_details(UId):
	try:
		data = UiUsersData([{'UId':UId}],deleted=True)
		data['user']=data['users'][0]
		data['user_types'] = user_types()
		rp_accs = Rp_acc.query\
			.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
				Rp_acc.UId==UId).all()
		rp_acc_list = []
		for rp_acc in rp_accs:
			obj={'RpAccId':rp_acc.RpAccId}
			rp_acc_list.append(obj)
		rp_accs = UiRpAccData(rp_acc_list,deleted=True)
		data['rp_acc_statuses'] = rp_acc_statuses()
		data['rp_acc_types'] = rp_acc_types()
	except Exception as ex:
		print(ex)
		return redirect(url_for('commerce_admin.users_table'))
	return render_template ("commerce/admin/user_details.html",
		**data,**rp_accs,title=gettext('Customer details'))

@bp.route("/admin/register_user",methods=['GET','POST'])
@login_required
@ui_admin_required()
def register_user():
	form = UserRegistrationForm()
	user_types_list = user_types()
	userTypeChoices=[]
	for user_type in user_types_list:
		obj=(user_type['UTypeId'],user_type['UTypeName'])
		userTypeChoices.append(obj)
	form.user_type.choices = userTypeChoices

	if form.validate_on_submit():
		print('validated')
		try:
			username = form.username.data
			email = form.email.data
			full_name = form.full_name.data
			user_type = form.user_type.data
			UShortName = (username[0]+username[-1]).upper()
			if Config.HASHED_PASSWORDS == True:
				password = bcrypt.generate_password_hash(form.password.data).decode() 
			else:
				password = form.password.data
			user = Users(
				UName=username,
				UEmail=email,
				UShortName=UShortName,
				UPass=password,
				UFullName=full_name,
				UTypeId=user_type)
			db.session.add(user)

			print(form.picture.data)
			if form.picture.data:
				imageFile = save_image(imageForm=form.picture.data,module=os.path.join("uploads","commerce","Users"),id=user.UId)
				lastImage = Image.query.order_by(Image.ImgId.desc()).first()
				ImgId = lastImage.ImgId+1
				image = Image(ImgId=ImgId,FileName=imageFile['FileName'],FilePath=imageFile['FilePath'],UId=user.UId)
				db.session.add(image)

			db.session.commit()

			flash('{} '.format(username)+lazy_gettext('successfully saved'),'success')
			return redirect(url_for('commerce_admin.users_table'))
		except Exception as ex:
			print(ex)
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_admin.register_user'))
	return render_template ("commerce/admin/register_user.html",
		form=form,title=gettext('Register'))

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
	OInvId = orderInvoice.OInvId
	orderInvRes = UiOInvData([{'OInvId':OInvId}])

	orderInvLines = Order_inv_line.query\
		.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),
									Order_inv_line.OInvId==OInvId)\
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


@bp.route("/admin/sale_repots_table")
@login_required
@ui_admin_required()
def sale_repots_table():
	return render_template ("commerce/admin/sale_repots_table.html",title=gettext('Sale reports'))

@bp.route("/admin/sale_repots_table2")
@login_required
@ui_admin_required()
def sale_repots_table2():
	return render_template ("commerce/admin/sale_repots_table2.html",title=gettext('Sale reports2'))
