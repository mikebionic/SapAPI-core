from flask import render_template, url_for, flash, redirect, request, session
from flask_login import current_user, login_user, logout_user
from datetime import datetime

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import db, gettext, lazy_gettext, bcrypt
from main_pack.base.apiMethods import get_login_info
# users and customers
from main_pack.models import User
from main_pack.commerce.auth.forms import AdminLoginForm
# / users and customers /
from main_pack.api.auth.attempt_counter import attempt_counter


@bp.route("/admin/login",methods=['GET','POST'])
@attempt_counter
def login():
	if (current_user.is_authenticated and "model_type" in session):
		if (session["model_type"] == "user" and current_user.is_admin):
			return redirect(url_for('commerce_admin.dashboard'))

	form = AdminLoginForm()
	if form.validate_on_submit():
		try:
			user = User.query.filter_by(
				GCRecord = None,
				UName = form.username.data,
				UTypeId = 1).first()

			if not user:
				raise Exception
			if not user.is_admin():
				raise Exception

			if Config.HASHED_PASSWORDS == True:
				password = bcrypt.check_password_hash(user.UPass, form.password.data)
			else:
				password = (user.UPass == form.password.data)

			if not password:
				raise Exception

			try:
				login_info = get_login_info(request)
				user.ULastActivityDate = login_info["date"]
				user.ULastActivityDevice = login_info["info"]
				db.session.commit()
			except Exception as ex:
				print(f"{datetime.now()} | User activity info update Exception: {ex}")

			session["model_type"] = "user"
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('commerce_admin.dashboard'))

		except Exception as ex:
			flash(lazy_gettext('Login Failed! Wrong username or password'),'danger')

	return render_template(
		f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/admin_login.html",
		url_prefix = url_prefix,
		title = gettext('Login'),
		form = form)


@bp.route("/admin/logout")
def logout():
	logout_user()
	return redirect(url_for('commerce_admin.login'))