from flask import render_template, url_for, json, jsonify, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.users import bp
from main_pack.commerce.users.forms import UpdateProfileForm,UpdateRpAccForm
from main_pack.commerce.users.utils import save_picture,commonUsedData

from main_pack.models.base.models import Image,Rp_acc

from functools import wraps
def admin_required():
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user:
				return redirect(url_for('commerce_auth.login'))
			elif not current_user.is_admin():
				flash(lazy_gettext('You do not have access to that page!'), 'danger')
				return redirect(url_for('commerce.commerce'))
			return f(*args, **kwargs)
		return decorated_function
	return decorator

@bp.route("/profile")
@login_required
def profile():
	commonData = commonUsedData()
	rpAcc = Rp_acc.query.filter(Rp_acc.RpAccId==current_user.UId).first()
	return render_template ("commerce/main/users/profile.html",**commonData,
		title=gettext('Profile'),rpAcc=rpAcc)

@bp.route("/profile_edit",methods=['GET', 'POST'])
@login_required
def profile_edit():
	form = UpdateRpAccForm()
	rpAcc = Rp_acc.query.filter(Rp_acc.UId==current_user.UId).first()
	
	if form.validate_on_submit():
		userData = {
			'UName':form.username.data,
			'UFullName':form.fullname.data
		}
		current_user.update(**userData)

		rpAccData = {
			'RpAccName':form.fullname.data,
			'RpAccAddress':form.address.data,
			'RpAccMobilePhoneNumber':form.mobilePhone.data,
			'RpAccHomePhoneNumber':form.homePhone.data,
			'RpAccZipCode':form.zipCode.data,
			# 'RpAccEMail':form.email.data
		}
		rpAcc.update(**rpAccData)

		db.session.commit()
		flash(lazy_gettext('Profile successfully updated!'), 'success')
		return redirect(url_for('commerce_users.profile'))
	elif request.method == 'GET':
		form.username.data = current_user.UName
		form.fullname.data = current_user.UFullName
		form.address.data = rpAcc.RpAccAddress
		form.mobilePhone.data = rpAcc.RpAccMobilePhoneNumber
		form.homePhone.data = rpAcc.RpAccHomePhoneNumber
		form.zipCode.data = rpAcc.RpAccZipCode
	commonData = commonUsedData()
	return render_template ("commerce/main/users/profile_edit.html",**commonData,
		title=gettext('Edit profile'),form=form)


@bp.route("/orders")
@login_required
def orders():
	commonData = commonUsedData()
	return render_template ("commerce/main/users/orders.html",**commonData,title=gettext('Orders'))

