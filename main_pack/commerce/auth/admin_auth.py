from flask import render_template, url_for, flash, redirect, request, session
from main_pack.commerce.auth import bp, url_prefix
from main_pack.config import Config

# useful methods
from main_pack import db, gettext, lazy_gettext, bcrypt
# / useful methods /

# auth and validation
from flask_login import current_user, login_user, logout_user
# / auth and validation /

# users and customers
from main_pack.models.users.models import Users
from main_pack.commerce.auth.forms import AdminLoginForm
# / users and customers /


@bp.route("/admin/login",methods=['GET','POST'])
def admin_login():
	if (current_user.is_authenticated and "user_type" in session):
		if (session["user_type"] == "user" and current_user.is_admin):
			return redirect(url_for('commerce_admin.dashboard'))

	form = AdminLoginForm()
	if form.validate_on_submit():
		try:
			user = Users.query.filter_by(GCRecord = None, UName = form.username.data).first()

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

			session["user_type"] = "user"
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
def admin_logout():
	logout_user()
	return redirect(url_for('commerce_auth.admin_login'))