from flask import render_template, url_for, json, jsonify, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db
from main_pack.commerce.users import bp
from main_pack.commerce.users.forms import UpdateProfileForm
from main_pack.commerce.users.utils import save_picture

@bp.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, "avatar")
			current_user.UImage = picture_file
		current_user.UName = form.username.data
		current_user.UFullName = form.fullname.data
		db.session.commit()
		flash('Profiliňiz üstünlikli üýtgedildi!', 'success')
		return redirect('/profile')
	elif request.method == 'GET':                                                                              
		form.username.data = current_user.UName
		form.fullname.data = current_user.UFullName
	return render_template('commerce/main/users/profile.html',title='Profili üýtget', form=form)
