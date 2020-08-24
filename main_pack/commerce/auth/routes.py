from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.auth import bp
from main_pack.config import Config

from main_pack.commerce.auth.forms import (LoginForm,RequestResetForm,ResetPasswordForm,
								RequestRegistrationForm,PasswordRegistrationForm)
from main_pack.models.users.models import Users,Rp_acc
from flask_login import login_user,current_user,logout_user
from main_pack import db,bcrypt,babel,gettext,lazy_gettext
from main_pack.commerce.auth.utils import (send_reset_email,get_register_token,
								verify_register_token,send_register_email)

from main_pack.commerce.commerce.utils import UiCategoriesList

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNo,generate,validate

@bp.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('commerce.commerce'))
	form = LoginForm()
	if form.validate_on_submit(): 
		user = Users.query.filter_by(UEmail=form.email.data).first()
		if user and bcrypt.check_password_hash(user.UPass,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('commerce.commerce'))
		else:
			flash(lazy_gettext('Login Failed! Wrong email or password'),'danger')
	
	categoryData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"auth/login.html",**categoryData,title=gettext('Login'), form=form)

@bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('commerce.commerce'))

@bp.route("/resetPassword", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('commerce.commerce'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(UEmail=form.email.data).first()
		send_reset_email(user)
		flash(lazy_gettext('An email has been sent with instructions to reset your password'),'info')
		return redirect(url_for('commerce_auth.login'))
	
	categoryData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"auth/reset_request.html",**categoryData,title=gettext('Reset Password'),form=form)

@bp.route("/resetPassword/<token>",methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('commerce.commerce'))
	user = Users.verify_reset_token(token)
	if user is None:
		flash(lazy_gettext('Token is invalid or expired'),'warning')
		return redirect(url_for('commerce_auth.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
		user.UPass = hashed_password
		db.session.commit()
		flash(lazy_gettext('Your password has been updated!'),'success')
		return redirect(url_for('commerce_auth.login'))

	categoryData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"auth/reset_token.html",**categoryData,title=gettext('Reset Password'),form=form)

@bp.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('commerce.commerce'))
	form = RequestRegistrationForm()
	if form.validate_on_submit():
		send_register_email(UName=form.username.data,UEmail=form.email.data)
		flash(lazy_gettext('An email has been sent with instructions to register your profile'),'info')
		return redirect(url_for('commerce_auth.register'))

	categoryData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"auth/register_request.html",**categoryData,title=gettext('Register'),form=form)

@bp.route("/register/<token>",methods=['GET','POST'])
def register_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('commerce.commerce'))
	new_user = verify_register_token(token)
	if not 'UEmail' in new_user:
		flash(lazy_gettext('Token is invalid or expired'),'warning')
		return redirect(url_for('commerce_auth.register'))
	form = PasswordRegistrationForm()
	if form.validate_on_submit():
		try:
			UName = new_user['UName']
			UEmail = new_user['UEmail']
			UShortName = (UName[0]+UName[-1]).upper()
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode() 
			user = Users(
				UName=UName,
				UEmail=UEmail,
				UShortName=UShortName,
				UPass=hashed_password,
				UFullName=form.full_name.data,
				UTypeId=5)
			db.session.add(user)

			# get the regNum for RpAccount registration
			try:
				reg_num = generate(UId=user.UId,prefixType='rp_code')
				regNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			except Exception as ex:
				flash(lazy_gettext('Error generating Registration number'),'warning')
				return redirect(url_for('commerce_auth.register'))
			# assign the UId of created User Model to Rp acc
			rp_acc = Rp_acc(
				RpAccUName=UName,
				RpAccUPass=hashed_password,
				RpAccName=form.full_name.data,
				RpAccEMail=UEmail,
				RpAccRegNo=regNo,
				RpAccTypeId=1,
				RpAccMobilePhoneNumber=form.phone_number.data,
				# UId=user.UId
				)
			db.session.add(rp_acc)
			# assign the RpAccId to a User model
			user.RpAccId = rp_acc.RpAccId
			db.session.commit()
			flash('{}!'.format(UName)+lazy_gettext('your profile has been created!'),'success')
			return redirect(url_for('commerce_auth.login'))
		except Exception as ex:
			flash(lazy_gettext('Error occured, please try again.'),'danger')
			return redirect(url_for('commerce_auth.register'))

	categoryData = UiCategoriesList()
	return render_template(Config.COMMERCE_TEMPLATES_FOLDER_PATH+"auth/register_token.html",**categoryData,title=gettext('Register'),form=form)