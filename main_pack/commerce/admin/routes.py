from flask import render_template,url_for,session,flash,redirect,request,Response,abort
import os
import uuid
from flask import current_app
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack.commerce.admin import bp, url_prefix
from main_pack.config import Config

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.languageMethods import dataLangSelector
# / useful methods /

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

# Company and Brand
from main_pack.models.base.models import Company
from main_pack.commerce.commerce.utils import UiBrandsList
from main_pack.models.commerce.models import Brand
# / Company and Brand /

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.admin.utils import resRelatedData
# / Resource and view /

# Invoices
from main_pack.models.commerce.models import (
	Inv_line,
	Inv_line_det,
	Inv_line_det_type,
	Inv_status,
	Inv_type,
	Invoice,
	Order_inv,
	Order_inv_line,
	Order_inv_type
)

from main_pack.commerce.commerce.order_utils import UiOInvData,UiOInvLineData
from main_pack.models.commerce.models import Res_category
# / Invoices /

# users and customers
from main_pack.models.users.models import (
	Users,
	User_type,
	Rp_acc,
	Rp_acc_type,
	Rp_acc_status
)

from main_pack.commerce.admin.users_utils import UiRpAccData, UiUsersData
from main_pack.commerce.admin.forms import (
	UserRegistrationForm,
	CustomerRegistrationForm,
	BrandForm
)
# / users and customers /

# RegNo
from main_pack.key_generator.utils import makeRegNo,generate,validate
from datetime import datetime,timezone
# / RegNo /

# Image operations
from main_pack.models.base.models import Image
from main_pack.base.imageMethods import save_image, save_icon
from main_pack.base.imageMethods import allowed_icon
# / Image operations /


@bp.route('/admin/language/<language>')
def set_language(language=None):
	session['language'] = language
	return redirect(url_for('commerce_admin.dashboard'))

@bp.route("/admin")

@bp.route("/admin/dashboard")
@login_required
@ui_admin_required
def dashboard():
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/dashboard.html",
		url_prefix = url_prefix,
		title = gettext('Dashboard'))


@bp.route("/admin/blank")
# @login_required
# @ui_admin_required
def hello():

	# browser = request.user_agent.browser
	# version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
	# platform = request.user_agent.platform
	# uas = request.user_agent.string
	# print(request.user_agent)
	# print('-------------')
	# print(browser)
	# print('-------------')
	# print(version)
	# print('-------------')
	# print(platform)
	# print('-------------')
	# print(uas)
	# print('-------------')


	print(session)
	return "Hekll world"


@bp.route("/admin/company")
@login_required
@ui_admin_required
def company():
	company = Company.query.get(1)
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/company.html",
		url_prefix = url_prefix,
		company = company,
		title = gettext('Company'))


@bp.route("/admin/category_table")
@login_required
@ui_admin_required
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
						"url": url_for('commerce_api.get_icon',category=folder,file_name=icon),
						"icon_name": icon,
						"category": folder
					}
					icons.append(iconInfo)
			category_icons[folder]=icons
		except Exception as ex:
			print(ex)
			print("Err: not a folder")

	data['category_icons']=category_icons
	categories = Res_category.query.filter_by(GCRecord = None).all()

	categoriesList = [category.to_json_api() for category in categories]
	data['categories'] = categoriesList if categoriesList else []
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/category_table.html",
		url_prefix = url_prefix,
		**data,
		title = gettext('Category table'))
###################################


@bp.route("/admin/resources_table")
@login_required
@ui_admin_required
def resources_table():
	resData=apiResourceInfo(showInactive=True,fullInfo=True,avoidQtyCheckup=True)
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/resources_table.html",
		url_prefix = url_prefix,
		**resData,
		title = gettext('Product table'))

def rp_acc_types():
	rp_acc_types = Rp_acc_type.query.filter_by(GCRecord = None).all()
	rp_acc_types_list = []
	for rp_acc_type in rp_acc_types:
		rp_acc_types_list.append(dataLangSelector(rp_acc_type.to_json_api()))
	return rp_acc_types_list

def rp_acc_statuses():
	rp_acc_statuses = Rp_acc_status.query.filter_by(GCRecord = None).all()
	rp_acc_statuses_list = []
	for rp_acc_status in rp_acc_statuses:
		rp_acc_statuses_list.append(dataLangSelector(rp_acc_status.to_json_api()))
	return rp_acc_statuses_list

def user_types():
	user_types = User_type.query.filter_by(GCRecord = None).all()
	user_types_list = []
	for user_type in user_types:
		user_types_list.append(dataLangSelector(user_type.to_json_api()))
	return user_types_list

##### customers table and customers information ######

@bp.route("/admin/customers_table")
@login_required
@ui_admin_required
def customers_table():
	data = UiRpAccData()
	data['rp_acc_statuses'] = rp_acc_statuses()
	data['rp_acc_types'] = rp_acc_types()
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/customers_table.html",
		url_prefix = url_prefix,
		**data,
		title = gettext('Customers'))


## !!! WARNING: Testing code
@bp.route("/admin/customers/")
# @login_required
# @ui_admin_required
def customers_json():
	data = UiRpAccData([{"RpAccId": 3}])
	data['rp_acc_statuses'] = rp_acc_statuses()
	data['rp_acc_types'] = rp_acc_types()

	return data
## !!! WARNING: Testing code


@bp.route("/admin/customer_details/<RpAccRegNo>")
@login_required
@ui_admin_required
def customer_details(RpAccRegNo):
	try:
		rp_acc = Rp_acc.query\
			.filter_by(RpAccRegNo = RpAccRegNo, GCRecord = None)\
			.options(
				joinedload(Rp_acc.users),
				joinedload(Rp_acc.rp_acc_status),
				joinedload(Rp_acc.rp_acc_type),
				joinedload(Rp_acc.Image),
				joinedload(Rp_acc.Order_inv))\
			.first()

		data = UiRpAccData(dbModels = [rp_acc])
		data['rp_acc'] = data['rp_accs'][0]
		data['rp_acc_statuses'] = rp_acc_statuses()
		data['rp_acc_types'] = rp_acc_types()

		# !!! TODO: this kinda functions UiOInvData sucks
		orders_list = []
		for orderInv in rp_acc.Order_inv:
			order = {}
			order['OInvId'] = orderInv.OInvId
			orders_list.append(order)
		orderInvRes = UiOInvData(orders_list)
	except Exception as ex:
		print(ex)
		return redirect(url_for('commerce_admin.customers_table'))

	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/customer_details.html",
		url_prefix = url_prefix,
		**data,**orderInvRes,
		title = gettext('Customer details'))


@bp.route("/admin/register_customer",methods=['GET','POST'])
@login_required
@ui_admin_required
def register_customer():
	form = CustomerRegistrationForm()

	customer_types_list = rp_acc_types()
	customerTypeChoices=[]
	for customer_type in customer_types_list:
		obj = (customer_type['RpAccTypeId'],customer_type['RpAccTypeName'])
		customerTypeChoices.append(obj)
	form.customer_type.choices = customerTypeChoices

	vendor_users = Users.query\
		.filter_by(GCRecord = None, RpAccId = None).all()
	vendorUserChoices=[]
	for vendor_user in vendor_users:
		obj = (vendor_user.UId,vendor_user.UName)
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

			last_User = Users.query.order_by(Users.UId.desc()).first()
			UId = last_User.UId+1
			user = Users(
				UId = UId,
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
					reg_num = generate(UId=vendor.UId,RegNumTypeName='rp_code')
					regNo = makeRegNo(vendor.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
				else:
					reg_num = generate(UId=user.UId,RegNumTypeName='rp_code')
					regNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			except Exception as ex:
				print(ex)
				regNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())

			last_RpAccId = Rp_acc.query.order_by(Rp_acc.RpAccId.desc()).first()
			RpAccId = last_RpAccId.UId+1
			rp_acc = Rp_acc(
				RpAccId = RpAccId,
				RpAccGuid = uuid.uuid4(),
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
				image = Image(
					ImgId = ImgId,
					ImgGuid = uuid.uuid4(),
					FileName = imageFile['FileName'],
					FilePath = imageFile['FilePath'],
					RpAccId = rp_acc.RpAccId)
				db.session.add(image)

			db.session.commit()

			flash('{} '.format(username)+lazy_gettext('successfully saved'),'success')
			return redirect(url_for('commerce_admin.customers_table'))
		except Exception as ex:
			print(ex)
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_admin.register_customer'))
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/register_customer.html",
		url_prefix = url_prefix,
		form=form,
		title = gettext('Register'))

################################

###### users and user information #####

@bp.route("/admin/users_table")
@login_required
@ui_admin_required
def users_table():
	data = UiUsersData()
	data['user_types'] = user_types()
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/users_table.html",
		url_prefix = url_prefix,
		**data,
		title = gettext('Users'))


@bp.route("/admin/user_details/<UId>")
@login_required
@ui_admin_required
def user_details(UId):
	try:
		data = UiUsersData([{"UId": UId}])
		data['user']=data['users'][0]
		data['user_types'] = user_types()
		# !!! TODO: Awful query... needs fix
		rp_accs = Rp_acc.query\
			.filter_by(GCRecord = None, UId = UId).all()
		rp_acc_list = []
		for rp_acc in rp_accs:
			obj={"RpAccId": rp_acc.RpAccId}
			rp_acc_list.append(obj)
		rp_accs = UiRpAccData(rp_acc_list)
		data['rp_acc_statuses'] = rp_acc_statuses()
		data['rp_acc_types'] = rp_acc_types()
	except Exception as ex:
		print(ex)
		return redirect(url_for('commerce_admin.users_table'))
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/user_details.html",
		url_prefix = url_prefix,
		**data,**rp_accs,
		title = gettext('Customer details'))


@bp.route("/admin/register_user",methods=['GET','POST'])
@login_required
@ui_admin_required
def register_user():
	form = UserRegistrationForm()
	user_types_list = user_types()
	userTypeChoices=[]
	for user_type in user_types_list:
		obj=(user_type['UTypeId'],user_type['UTypeName'])
		userTypeChoices.append(obj)
	form.user_type.choices = userTypeChoices

	if form.validate_on_submit():
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
			last_User = Users.query.order_by(Users.UId.desc()).first()
			UId = last_User.UId+1
			user = Users(
				UId = UId,
				UGuid = uuid.uuid4(),
				UName = username,
				UEmail = email,
				UShortName = UShortName,
				UPass = password,
				UFullName = full_name,
				UTypeId = user_type)
			db.session.add(user)

			if form.picture.data:
				imageFile = save_image(imageForm=form.picture.data,module=os.path.join("uploads","commerce","Users"),id=user.UId)
				lastImage = Image.query.order_by(Image.ImgId.desc()).first()
				ImgId = lastImage.ImgId+1
				image = Image(
					ImgId = ImgId,
					ImgGuid = uuid.uuid4(),
					FileName = imageFile['FileName'],
					FilePath = imageFile['FilePath'],
					UId = user.UId)
				db.session.add(image)

			db.session.commit()

			flash('{} '.format(username)+lazy_gettext('successfully saved'),'success')
			return redirect(url_for('commerce_admin.users_table'))
		except Exception as ex:
			print(ex)
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_admin.register_user'))
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/register_user.html",
		url_prefix = url_prefix,
		form=form,
		title = gettext('Register'))

#################################


###### orders and order information #######
@bp.route("/admin/order_invoices")
@login_required
@ui_admin_required
def order_invoices():
	InvStatId = request.args.get("statusId",1,type=int)
	orderInvoices = Order_inv.query\
		.filter_by(GCRecord = None, InvStatId = InvStatId)\
		.order_by(Order_inv.ModifiedDate.desc()).all()
	
	orders_list = []
	for orderInv in orderInvoices:
		order = {}
		order['OInvId'] = orderInv.OInvId
		orders_list.append(order)
	orderInvRes = UiOInvData(orders_list)
	
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()
	invoice_statuses = []
	for inv_stat in inv_statuses:
		invoice_statuses.append(dataLangSelector(inv_stat.to_json_api()))
	InvoiceStatuses = {"inv_statuses": invoice_statuses}

	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/order_invoices.html",
		url_prefix = url_prefix,
		**orderInvRes,**InvoiceStatuses,InvStatId=InvStatId,
		title = gettext('Order invoices'))


@bp.route("/admin/order_invoices/<OInvRegNo>",methods=['GET','POST'])
@login_required
@ui_admin_required
def order_inv_lines(OInvRegNo):
	orderInvoice = Order_inv.query\
		.filter_by(GCRecord = None, OInvRegNo = OInvRegNo)\
		.first()
	OInvId = orderInvoice.OInvId
	orderInvRes = UiOInvData([{"OInvId": OInvId}])

	orderInvLines = Order_inv_line.query\
		.filter_by(GCRecord = None, OInvId = OInvId)\
		.order_by(Order_inv_line.CreatedDate.desc()).all()

	order_lines_list = []
	for orderInvLine in orderInvLines:
		order_inv_line = {}
		order_inv_line['OInvLineId'] = orderInvLine.OInvLineId
		order_lines_list.append(order_inv_line)
	orderInvLineRes = UiOInvLineData(order_lines_list)
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()
	invoice_statuses = []
	for inv_stat in inv_statuses:
		invoice_statuses.append(dataLangSelector(inv_stat.to_json_api()))
	InvoiceStatuses = {"inv_statuses": invoice_statuses}
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/order_inv_lines.html",
		url_prefix = url_prefix,
		**orderInvLineRes,**InvoiceStatuses,**orderInvRes,
		title = gettext('Order invoices'))
#########################################


@bp.route("/admin/add_product")
@login_required
@ui_admin_required
def add_product():
	resData=resRelatedData()
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/add_product.html",
		url_prefix = url_prefix,
		**resData,
		title = gettext('Add product'))


@bp.route("/admin/sale_repots_table")
@login_required
@ui_admin_required
def sale_repots_table():
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/sale_repots_table.html",
		url_prefix = url_prefix,
		title = gettext('Sale reports'))


@bp.route("/admin/sale_repots_table2")
@login_required
@ui_admin_required
def sale_repots_table2():
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/sale_repots_table2.html",
		url_prefix = url_prefix,
		title = gettext('Sale reports'))


@bp.route("/admin/brands_table")
@login_required
@ui_admin_required
def brands_table():
	res = UiBrandsList()
	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/brands_table.html",
		url_prefix = url_prefix,
		**res,
		title = gettext('Brands'))


@bp.route("/admin/manage_brand",methods=['GET','POST'])
@login_required
@ui_admin_required
def manage_brand():
	BrandId = request.args.get('brandId')
	manage_mode = "create"
	form = BrandForm()
	brand = None
	if BrandId:
		brand = Brand.query\
			.filter_by(GCRecord = None, BrandId = BrandId)\
			.first()
		if brand:
			manage_mode = "update"

	if form.validate_on_submit():
		try:
			brand_data = {
				"BrandName": form.BrandName.data,
				"BrandDesc": form.BrandDesc.data,
				"BrandVisibleIndex": form.BrandVisibleIndex.data if isinstance(form.BrandVisibleIndex.data,int) else None,
				"IsMain": form.IsMain.data,
				"BrandLink1": form.BrandLink1.data,
				"BrandLink2": form.BrandLink2.data,
				"BrandLink3": form.BrandLink3.data,
				"BrandLink4": form.BrandLink4.data,
				"BrandLink5": form.BrandLink5.data
			}
			
			if manage_mode == "update":
				brand.update(**brand_data)
			else:
				brand = Brand(**brand_data)
				db.session.add(brand)
			
			db.session.commit()

			if form.Image.data:
				imageFile = save_icon(imageForm=form.Image.data,module=os.path.join("uploads","commerce","Brand"),id=brand.BrandId)
				lastImage = Image.query.order_by(Image.ImgId.desc()).first()
				ImgId = lastImage.ImgId+1
				image = Image(
					ImgId = ImgId,
					ImgGuid = uuid.uuid4(),
					FileName = imageFile['FileName'],
					FilePath = imageFile['FilePath'],
					BrandId = brand.BrandId)
				db.session.add(image)

			db.session.commit()

			flash('{} '.format(brand.BrandName)+lazy_gettext('successfully saved'),'success')
			return redirect(url_for('commerce_admin.brands_table'))
		except Exception as ex:
			print(ex)
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_admin.manage_brand'))

	if brand:
		form.BrandName.data = brand.BrandName
		form.BrandDesc.data = brand.BrandDesc
		form.BrandVisibleIndex.data = brand.BrandVisibleIndex
		form.IsMain.data = brand.IsMain
		form.BrandLink1.data = brand.BrandLink1
		form.BrandLink2.data = brand.BrandLink2
		form.BrandLink3.data = brand.BrandLink3
		form.BrandLink4.data = brand.BrandLink4
		form.BrandLink5.data = brand.BrandLink5

	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/manage_brand.html",
		url_prefix = url_prefix,
		form=form,
		title = gettext('Brand'))