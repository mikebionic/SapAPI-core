from flask import (
	render_template,
	url_for,
	session,
	flash,
	redirect,
	request,
)
from flask_login import login_user, current_user, logout_user
from datetime import datetime
import uuid

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import db, gettext, lazy_gettext

# forms
from main_pack.commerce.auth.forms import (
	LoginForm,
	RequestResetForm,
	ResetPasswordForm,
	RequestRegistrationForm,
	PasswordRegistrationForm)

# db Models
from main_pack.models import Rp_acc

# utils
from main_pack.commerce.auth.utils import (
	send_reset_email,
	verify_register_token,
	send_register_email,
)
from main_pack.api.auth.attempt_counter import attempt_counter

from main_pack.commerce.commerce.utils import UiCategoriesList
from main_pack.base.apiMethods import get_login_info
from main_pack.base import log_print

from main_pack.api.common import (
	configurePassword,
	checkPassword,
	configurePhoneNumber,
	gather_required_register_rp_acc_data,
)

@bp.route("/login",methods=['GET','POST'])
@attempt_counter
def login():
	form = LoginForm()

	if form.validate_on_submit():
		try:
			user = Rp_acc.query.filter_by(RpAccEMail = form.email.data, GCRecord = None).first()

			if not user:
				raise Exception

			if not checkPassword(user.RpAccUPass, form.password.data):
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
				password = configurePassword(form.password.data)
				if password:
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
		password = configurePassword(form.password.data)
		if password:
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

			RpAccUName = new_user['username']
			RpAccEMail = new_user['email']
			
			password = configurePassword(form.password.data)
			if not password:
				log_print("Register token exception, password not valid", "warning")
				raise Exception

			RpAccUPass = password
			RpAccMobilePhoneNumber = configurePhoneNumber(form.phone_number.data)
			RpAccName = form.full_name.data.strip() if form.full_name.data else ""
			RpAccAddress = form.address.data if form.address.data else None

			check_registration = Rp_acc.query\
				.filter_by(
					RpAccEMail = RpAccEMail,
					RpAccUName = RpAccUName,
					GCRecord = None)\
				.first()
			if check_registration:
				raise Exception

			UId, CId, DivId, RpAccRegNo, RpAccGuid = gather_required_register_rp_acc_data()

			rp_acc_data = {
				"UId": UId,
				"CId": CId,
				"DivId": DivId,
				"RpAccGuid": RpAccGuid,
				"RpAccUName": RpAccUName,
				"RpAccEMail": RpAccEMail,
				"RpAccUPass": RpAccUPass,
				"RpAccName": RpAccName,
				"RpAccRegNo": RpAccRegNo,
				"RpAccMobilePhoneNumber": RpAccMobilePhoneNumber,
				"RpAccAddress": RpAccAddress,
				"RpAccTypeId": 2,
				"RpAccStatusId": 1,
			}

			lastUser = Rp_acc.query.order_by(Rp_acc.RpAccId.desc()).first()
			RpAccId = lastUser.RpAccId + 1
			rp_acc_data["RpAccId"] = RpAccId,

			user = Rp_acc(**rp_acc_data)
			db.session.add(user)

			try:
				login_info = get_login_info(request)
				user.RpAccLastActivityDate = login_info["date"]
				user.RpAccLastActivityDevice = login_info["info"]
			except Exception as ex:
				print(f"{datetime.now()} | Rp_acc activity info update Exception: {ex}")

			db.session.commit()

			flash("{}, {}".format(RpAccUName, lazy_gettext('your profile has been created!')),'success')
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


@bp.route("/register-sms",methods=['GET','POST'])
def register_sms():
	if (current_user.is_authenticated and "model_type" in session):
		if session["model_type"] == "rp_acc":
			return redirect(url_for('commerce.commerce'))

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/auth/register_sms.html",
		**categoryData,
		api_url_prefix = Config.API_URL_PREFIX,
		url_prefix = url_prefix,
		title = "{} - {}".format(gettext('Register'), "SMS"),
	)