from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response
from main_pack.commerce.admin.forms import LogoImageForm,SliderImageForm
from main_pack.commerce.admin.image_utils import save_picture
from main_pack.commerce.admin import bp
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext

@bp.route("/images_setup", methods=['GET', 'POST'])
@login_required
def images_setup():
	logoForm = LogoImageForm()
	sliderForm = SliderImageForm()
	if logoForm.validate_on_submit():
		if logoForm.logoImage.data:
			print('posting logo')
			picture_file = save_picture(logoForm.logoImage.data,"",'logo')
			print(picture_file)
		flash(lazy_gettext('Company logo successfully uploaded!'), 'success')
		return redirect(url_for('commerce_admin.images_setup'))
	if sliderForm.validate_on_submit():
		if sliderForm.sliderImage.data:
			print('posting slider')
			picture_file = save_picture(sliderForm.sliderImage.data,"",'')
			print(picture_file)
		flash(lazy_gettext('Slider picture successfully uploaded!'),'success')
		return redirect(url_for('commerce_admin.images_setup'))
	return render_template('commerce/admin/images_setup.html',title=gettext('Setup images'),
		logoForm=logoForm,sliderForm=sliderForm)
