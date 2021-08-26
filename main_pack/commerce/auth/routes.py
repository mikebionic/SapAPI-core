from flask import render_template, url_for, jsonify, session, flash, redirect, request, Response, abort
from flask_login import login_user, current_user, logout_user
from datetime import datetime
import uuid

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import db, bcrypt, gettext, lazy_gettext

# forms
from main_pack.commerce.auth.forms import (
	LoginForm,
	RequestResetForm,
	ResetPasswordForm,
	RequestRegistrationForm,
	PasswordRegistrationForm)

# db Models
from main_pack.models import User, Rp_acc
from main_pack.models import (
	Company,
	Division,
)

# utils
from main_pack.commerce.auth.utils import (
	send_reset_email,
	get_register_token,
	verify_register_token,
	send_register_email,
)
from main_pack.api.auth.attempt_counter import attempt_counter

from main_pack.commerce.commerce.utils import UiCategoriesList
from main_pack.key_generator.utils import makeRegNo, generate
from main_pack.base.apiMethods import get_login_info


@bp.route("/login",methods=['GET','POST'])
@attempt_counter
def login():
	form = LoginForm()

	if form.validate_on_submit():
		try:
			user = Rp_acc.query.filter_by(RpAccEMail = form.email.data, GCRecord = None).first()

			if not user:
				raise Exception

			if Config.HASHED_PASSWORDS == True:
				password = bcrypt.check_password_hash(user.RpAccUPass, form.password.data)
			else:
				password = (user.RpAccUPass == form.password.data)

			if not password:
				raise Exception

			try:
				login_info = get_login_info(request)
				user.RpAccLastActivityDate = login_info["date"]
				user.RpAccLastActivityDevice = login_info["info"]
				db.session.commit()
			except Exception as ex:
				print(f"{datetime.now()} | Rp_acc activity info update Exception: {ex}")

			session["model_type"] = "rp_acc"
			session["ResPriceGroupId"] = user.ResPriceGroupId
			login_user(user, remember=form.remember.data)
			next_page = request.args.get("next")

			return redirect(next_page) if next_page else redirect(url_for('commerce.commerce'))

		except Exception as ex:
			flash(lazy_gettext('Login Failed! Wrong email or password'),'danger')

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/login.html",
		**categoryData,
		url_prefix = url_prefix,
		title = gettext('Login'),
		form = form)


@bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('commerce.commerce'))


@bp.route("/resetPassword", methods=['GET','POST'])
def reset_request():
	categoryData = UiCategoriesList()
	if (current_user.is_authenticated and "model_type" in session):
		if session["model_type"] == "rp_acc":
			form = ResetPasswordForm()

			if form.validate_on_submit():
				if Config.HASHED_PASSWORDS == True:
					password = bcrypt.generate_password_hash(form.password.data).decode()
				else:
					password = form.password.data

				current_user.RpAccUPass = password
				db.session.commit()
				flash(lazy_gettext('Your password has been updated!'),'success')
				return redirect(url_for('commerce.commerce'))

			return render_template(
				f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/reset_token.html",
				**categoryData,
				url_prefix = url_prefix,
				title = gettext('Reset password'),
				form = form)

	form = RequestResetForm()
	if form.validate_on_submit():
		user = Rp_acc.query.filter_by(RpAccEMail = form.email.data, GCRecord = None).first()

		send_reset_email(user, model_type="rp_acc")
		flash(lazy_gettext('An email has been sent with instructions to reset your password'),'info')

		return redirect(url_for('commerce_auth.login'))

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/reset_request.html",
		**categoryData,
		url_prefix = url_prefix,
		title = gettext('Reset password'),
		form = form)


@bp.route("/resetPassword/<token>",methods=['GET','POST'])
def reset_token(token):
	user = Rp_acc.verify_reset_token(token)

	if user is None:
		flash(lazy_gettext('Token is invalid or expired'),'warning')
		return redirect(url_for('commerce_auth.reset_request'))

	form = ResetPasswordForm()
	if form.validate_on_submit():

		if Config.HASHED_PASSWORDS == True:
			password = bcrypt.generate_password_hash(form.password.data).decode()
		else:
			password = form.password.data

		user.RpAccUPass = password
		db.session.commit()
		flash(lazy_gettext('Your password has been updated!'),'success')
		login_user(user)
		return redirect(url_for('commerce.commerce'))

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/reset_token.html",
		**categoryData,
		url_prefix = url_prefix,
		title = gettext('Reset password'),
		form = form)


@bp.route("/register",methods=['GET','POST'])
def register():
	if (current_user.is_authenticated and "model_type" in session):
		if session["model_type"] == "rp_acc":
			return redirect(url_for('commerce.commerce'))

	form = RequestRegistrationForm()
	if form.validate_on_submit():
		send_register_email(username = form.username.data, email = form.email.data)
		flash(lazy_gettext('An email has been sent with instructions to register your profile'),'info')
		return redirect(url_for('commerce_auth.register'))

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/register_request.html",
		**categoryData,
		url_prefix = url_prefix,
		title = gettext('Register'),
		form = form)


@bp.route("/register/<token>",methods=['GET','POST'])
def register_token(token):
	if (current_user.is_authenticated and "model_type" in session):
		if session["model_type"] == "rp_acc":
			return redirect(url_for('commerce.commerce'))

	new_user = verify_register_token(token)

	if not new_user:
		flash(lazy_gettext('Token is invalid or expired'),'warning')
		return redirect(url_for('commerce_auth.register'))

	form = PasswordRegistrationForm()
	if form.validate_on_submit():
		try:
			username = new_user['username']
			email = new_user['email']

			if Config.HASHED_PASSWORDS == True:
				password = bcrypt.generate_password_hash(form.password.data).decode()
			else:
				password = form.password.data

			check_registration = Rp_acc.query\
				.filter_by(
					RpAccEMail = email,
					RpAccUName = username,
					GCRecord = None)\
				.first()
			if check_registration:
				raise Exception

			lastUser = Rp_acc.query.order_by(Rp_acc.RpAccId.desc()).first()
			RpAccId = lastUser.RpAccId + 1

			main_user = User.query\
				.filter_by(GCRecord = None, UTypeId = 1)\
				.first()

			try:
				reg_num = generate(UId=main_user.UId, RegNumTypeName='rp_code')
				regNo = makeRegNo(main_user.UShortName, reg_num.RegNumPrefix, reg_num.RegNumLastNum + 1, '',RegNumTypeName='rp_code')
				reg_num.RegNumLastNum = reg_num.RegNumLastNum + 1
				db.session.commit()
			except Exception as ex:
				print(f"{datetime.now()} | UI Register Reg Num generation Exception: {ex}")
				regNo = str(datetime.now().timestamp())
				# flash(lazy_gettext('Error generating Registration number'),'warning')
				# return redirect(url_for('commerce_auth.register'))

			company = Company.query.filter_by(CGuid = Config.MAIN_CGUID).first()
			if not company:
				company = Company.query.first()

			division = Division.query.filter_by(DivGuid = Config.C_REGISTRATION_DIVGUID).first()
			if not division:
				division = Division.query.first()

			CId = company.CId if company else None
			DivId = division.DivId if division else None

			user_data = {
				"RpAccId": RpAccId,
				"UId": main_user.UId,
				"RpAccGuid": uuid.uuid4(),
				"RpAccUName": username,
				"RpAccEMail": email,
				"RpAccUPass": password,
				"RpAccName": form.full_name.data,
				"RpAccRegNo": regNo,
				"RpAccTypeId": 2,
				"RpAccMobilePhoneNumber": form.phone_number.data,
				"RpAccAddress": form.address.data if form.address.data else None,
				"CId": CId,
				"DivId": DivId,
				"RpAccStatusId": 1
			}

			user = Rp_acc(**user_data)
			db.session.add(user)

			try:
				login_info = get_login_info(request)
				user.RpAccLastActivityDate = login_info["date"]
				user.RpAccLastActivityDevice = login_info["info"]
			except Exception as ex:
				print(f"{datetime.now()} | Rp_acc activity info update Exception: {ex}")

			db.session.commit()

			flash("{}, {}".format(username, lazy_gettext('your profile has been created!')),'success')
			session["model_type"] = "rp_acc"
			session["ResPriceGroupId"] = user.ResPriceGroupId
			login_user(user)
			return redirect(url_for('commerce.commerce'))

		except Exception as ex:
			print(f"{datetime.now()} | UI Register Exception: {ex}")
			flash(lazy_gettext('Error occured, please try again.'), 'danger')
			return redirect(url_for('commerce_auth.register'))

	flash(lazy_gettext("Please, proceed the registration"), "warning")
	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/register_token.html",
		**categoryData,
		url_prefix = url_prefix,
		title = gettext('Register'),
		form = form)