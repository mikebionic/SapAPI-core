from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response
from main_pack.base.imageMethods import save_image,save_icon
from main_pack.commerce.admin import bp
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext

from main_pack.models.base.models import Company,Sl_image,Slider,Image
from sqlalchemy import or_, and_
import os

from main_pack.commerce.admin.forms import LogoImageForm,SliderImageForm

@bp.route("/admin/images_setup", methods=['GET', 'POST'])
@login_required
def images_setup():
	company = Company.query.get(1)
	
	company_logo = Image.query.filter(and_(Image.CId==company.CId, Image.GCRecord==None)).order_by(Image.CreatedDate.desc()).first()

	logoForm = LogoImageForm()

	if "logoForm" in request.form and logoForm.validate_on_submit():
		if logoForm.logoImage.data:
			imageFile = save_icon(imageForm=logoForm.logoImage.data,module=os.path.join("uploads","commerce","Company"),id=company.CId)
			
			lastImage = Image.query.order_by(Image.ImgId.desc()).first()
			ImgId = lastImage.ImgId+1
			image = Image(ImgId=ImgId,FileName=imageFile['FileName'],FilePath=imageFile['FilePath'],CId=company.CId)
			db.session.add(image)
			db.session.commit()

		flash(lazy_gettext('Company logo successfully uploaded!'), 'success')
		return redirect(url_for('commerce_admin.images_setup'))
	return render_template('commerce/admin/images_setup.html',title=gettext('Setup images'),
		logoForm=logoForm,company_logo=company_logo)

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
	# handler for commerce view
	header_slider = Slider.query\
		.filter(and_(Slider.GCRecord=='' or Slider.GCRecord==None),Slider.SlName=='commerce_header').first()
	if header_slider is None:
		# create a commerce_header for header slider automatically
		slider = Slider(SlName="commerce_header")
		db.session.add(slider)
		db.session.commit()

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

@bp.route("/admin/sliders/<SlId>", methods=['GET', 'POST'])
@login_required
def slider_images(SlId):
	slider = Slider.query\
		.filter(and_(Slider.GCRecord=='' or Slider.GCRecord==None),Slider.SlId==SlId).first()
	if slider:
		print(slider.SlName)
		sl_images = Sl_image.query.filter(and_(Sl_image.SlId==slider.SlId, Sl_image.GCRecord==None)).all()
		sliderForm = SliderImageForm()

		if "sliderForm" in request.form and sliderForm.validate_on_submit():
			if sliderForm.sliderImage.data:

				imageFile = save_image(imageForm=sliderForm.sliderImage.data,module=os.path.join("uploads","commerce","Slider"),id=slider.SlId)
				image = Sl_image(
					SlImgName=imageFile['FileName'],
					SlImgDesc=sliderForm.sliderImageDesc.data,
					SlImgMainImgFileName=imageFile['FilePath'],				
					SlId=slider.SlId)
				db.session.add(image)
				db.session.commit()

			flash(lazy_gettext('Slider picture successfully uploaded!'),'success')
			return redirect(url_for('commerce_admin.slider_images',SlId=slider.SlId))
	else:
		return redirect(url_for('commerce_admin.sliders'))
	return render_template('commerce/admin/slider_setup.html',title=gettext('Setup images'),
		sliderForm=sliderForm,slider=slider,sl_images=sl_images)


@bp.route('/ui/svg-icons/',methods=['POST'])
def ui_svg_icons():
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	files = request.files.getlist('files[]')
	uploadedFiles=[]
	failedFiles=[]
	
	for icon_file in icon_files:
		if icon_file and allowed_file(icon_file.filename):
			imageFile = save_icon(imageForm=icon_file,module=os.path.join("commerce","icons","categories","Others"))
			FileName = image['FileName']
			FilePath = image['FilePath']
			uploadedFiles.append({
				'fileName':FileName,
				'htmlData':render_template('/commerce/admin/imageAppend.html',
					FileName=FileName,FilePath=FilePath),
			})
		else:
			failedFiles.append({
				'fileName':icon_file.fileName
			})

	response = jsonify({
		"data":uploadedFiles,
		"total":len(uploadedFiles),
		"failed":failedFiles,
		"failedTotal":len(failedFiles)
		})
	return response
