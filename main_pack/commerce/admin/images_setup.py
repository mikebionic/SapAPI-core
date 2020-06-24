from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response
from main_pack.commerce.admin.forms import LogoImageForm,SliderImageForm
from main_pack.base.imageMethods import save_image
from main_pack.commerce.admin import bp
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext

from main_pack.models.base.models import Company,Sl_image,Slider,Image
from sqlalchemy import or_, and_
import os

@bp.route("/admin/images_setup", methods=['GET', 'POST'])
@login_required
def images_setup():
	company = Company.query.get(1)
	slider = Slider.query.get(1)

	# I will leave it here for a while
	if not slider:
		slider = Slider(SlName="Nav slider",CId=1)
		db.session.add(slider)
		db.session.commit()

	sl_images = Sl_image.query.filter(and_(Sl_image.SlId==slider.SlId, Sl_image.GCRecord==None)).all()

	company_logo = Image.query.filter(and_(Image.CId==company.CId, Image.GCRecord==None)).order_by(Image.CreatedDate.desc()).first()

	sliderForm = SliderImageForm()
	logoForm = LogoImageForm()

	if "sliderForm" in request.form and sliderForm.validate_on_submit():
		if sliderForm.sliderImage.data:

			imageFile = save_image(imageForm=sliderForm.sliderImage.data,module=os.path.join("uploads","commerce","Slider"),id=slider.SlId)
			image = Sl_image(SlImgName=imageFile['FileName'],SlImgMainImgFileName=imageFile['FilePath'],SlId=slider.SlId)
			db.session.add(image)
			db.session.commit()

		flash(lazy_gettext('Slider picture successfully uploaded!'),'success')
		return redirect(url_for('commerce_admin.images_setup'))

	if "logoForm" in request.form and logoForm.validate_on_submit():
		if logoForm.logoImage.data:

			imageFile = save_image(imageForm=logoForm.logoImage.data,module=os.path.join("uploads","commerce","Company"),id=company.CId)
			image = Image(FileName=imageFile['FileName'],FilePathR=imageFile['FilePathR'],FilePathM=imageFile['FilePathM'],
				FilePathS=imageFile['FilePathS'],CId=company.CId)
			db.session.add(image)
			db.session.commit()

		flash(lazy_gettext('Company logo successfully uploaded!'), 'success')
		return redirect(url_for('commerce_admin.images_setup'))
	return render_template('commerce/admin/images_setup.html',title=gettext('Setup images'),
		logoForm=logoForm,sliderForm=sliderForm,sl_images=sl_images,company_logo=company_logo)

@bp.route("/remove_images")
@login_required
def remove_images():
	try:
		imgId = request.args.get('imgId')
		imgType = request.args.get('type')
		if imgType == 'logo':
			image = Image.query.get(imgId)
			image.GCRecord=1
			db.session.commit()
		elif imgType == 'slider':
			sl_image = Sl_image.query.get(imgId)
			sl_image.GCRecord = 1
			db.session.commit()

		flash("Image successfully deleted!",'success')
	except:
		flash("Error, unable to execute this",'warning')
	return redirect(url_for('commerce_admin.images_setup'))


@bp.route("/admin/sliders", methods=['GET', 'POST'])
@login_required
def sliders():

	sliders = Slider.query\
		.filter(Slider.GCRecord=='' or Slider.GCRecord==None).all()
	slidersData = []
	for slider in sliders:
		sliderList = slider.to_json_api()

		sl_images = Sl_image.query\
			.filter(and_(Sl_image.SlId==slider.SlId,Sl_image.GCRecord==None)).all()
		
		slider_images = []
		for sl_image in sl_images:
			slider_images.append(sl_image.to_json_api())

		sliderList["Sl_images"] = slider_images
		slidersData.append(sliderList)

	return render_template('commerce/admin/sliders.html',title=gettext('Setup images'),
		sliders=slidersData)