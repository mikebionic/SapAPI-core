from flask import render_template,url_for,session,flash,redirect,request,Response,abort
from main_pack.commerce.admin import bp
import os
from flask import current_app
from main_pack.config import Config

# useful methods
from main_pack import db,babel,gettext,lazy_gettext,bcrypt
from main_pack.base.languageMethods import dataLangSelector
from sqlalchemy import and_
# / useful methods /

# auth and validation
from flask_login import current_user,login_required,login_user,logout_user
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

# users and customers
from main_pack.models.users.models import (Users,User_type,
																					Rp_acc,Rp_acc_type,Rp_acc_status)
from main_pack.commerce.admin.users_utils import UiRpAccData,UiUsersData
from main_pack.commerce.admin.forms import UserRegistrationForm,CustomerRegistrationForm
from main_pack.commerce.admin.forms import LoginForm
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

@bp.route("/admin/login")
def login():
	if current_user.is_authenticated:
		return redirect(url_for('commerce_admin.dashboard'))
	form = LoginForm()
	if form.validate_on_submit(): 
		user = Users.query.filter_by(UEmail=form.email.data).first()
		if Config.HASHED_PASSWORDS == True:
			password = bcrypt.check_password_hash(user.UPass,form.password.data)
		else:
			password = (user.UPass == form.password.data)
			print('no hashing conditions')
			print(password)
		if user and password:
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('commerce_admin.dashboard'))
		else:
			flash(lazy_gettext('Login Failed! Wrong email or password'),'danger')
	return render_template ("commerce/admin/login.html",title=gettext('Login'),form=form)

@bp.route("/admin/logout")
def logout():
	logout_user()
	return redirect(url_for('commerce_admin.login'))

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