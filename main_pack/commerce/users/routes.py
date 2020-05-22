from flask import render_template, url_for, json, jsonify, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.users import bp
from main_pack.commerce.users.forms import UpdateProfileForm
from main_pack.commerce.users.utils import save_picture,commonUsedData

from main_pack.models.base.models import Image

@bp.route("/profile")
@login_required
def profile():
	commonData = commonUsedData()
	# rpAcc = Rp_acc.query.filter(Rp_acc.RpAccId==current_user.UId)
	return render_template ("commerce/main/users/profile.html",**commonData,title=gettext('Profile'))

@bp.route("/profile_edit",methods=['GET', 'POST'])
@login_required
def profile_edit():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		userData = {
			'UName':form.username.data,
			'UFullName':form.fullname.data
		}
		current_user.update(**userData)
		db.session.commit()
		flash('Profile successfully updated!', 'success')
		return redirect('/profile')
	elif request.method == 'GET':
		form.username.data = current_user.UName
		form.fullname.data = current_user.UFullName
	commonData = commonUsedData()
	return render_template ("commerce/main/users/profile_edit.html",**commonData,
		title=gettext('Edit profile'),form=form)


@bp.route("/orders")
@login_required
def orders():
	commonData = commonUsedData()
	return render_template ("commerce/main/users/orders.html",**commonData,title=gettext('Orders'))

