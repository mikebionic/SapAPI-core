from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response
from main_pack.base.imageMethods import save_image,save_icon,allowed_icon,allowed_image
from main_pack.base.dataMethods import dateDataCheck
from main_pack.commerce.admin import bp, url_prefix

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from main_pack import db,babel,gettext,lazy_gettext
from flask import current_app
from main_pack.models.base.models import Company,Sl_image,Slider,Image
from sqlalchemy import or_, and_
import os

from main_pack.commerce.admin.forms import LogoImageForm,SliderImageForm

@bp.route("/admin/logo_setup", methods=['GET', 'POST'])
@login_required
@ui_admin_required()
def logo_setup():
	company = Company.query\
		.filter(Company.GCRecord=='' or Company.GCRecord==None).first()
	company_logo = Image.query\
		.filter(and_(Image.CId==company.CId,Image.GCRecord==None))\
		.order_by(Image.CreatedDate.desc()).first()
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
		return redirect(url_for('commerce_admin.logo_setup'))
	return render_template('commerce/admin/logo_setup.html',url_prefix=url_prefix,
		title=gettext('Company logo'),logoForm=logoForm,company_logo=company_logo)

@bp.route("/remove_images")
@login_required
@ui_admin_required()
def remove_images():
	try:
		imgId = request.args.get('imgId')
		imgType = request.args.get('type')
		if imgType == 'logo':
			image = Image.query.get(imgId)
			image.GCRecord=1
			db.session.commit()
			url = url_for('commerce_admin.logo_setup')
		elif imgType == 'slider':
			sl_image = Sl_image.query.get(imgId)
			sl_image.GCRecord = 1
			db.session.commit()
			url = url_for('commerce_admin.sliders')

		flash("Image successfully deleted!",'success')
	except Exception as ex:
		print(ex)
		flash("Error, unable to execute this",'warning')
	return redirect(url)

@bp.route("/admin/sliders", methods=['GET', 'POST'])
@login_required
@ui_admin_required()
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

	return render_template('commerce/admin/sliders.html',url_prefix=url_prefix,
		title=gettext('Sliders'),sliders=slidersData)

@bp.route("/admin/sliders/<SlId>", methods=['GET', 'POST'])
@login_required
@ui_admin_required()
def slider_images(SlId):
	slider = Slider.query\
		.filter(and_(Slider.GCRecord=='' or Slider.GCRecord==None),Slider.SlId==SlId).first()
	if slider:
		sl_images = Sl_image.query.filter(and_(Sl_image.SlId==slider.SlId, Sl_image.GCRecord==None)).all()
		sliderForm = SliderImageForm()

		if "sliderForm" in request.form and sliderForm.validate_on_submit():
			print(request.form)
			if sliderForm.sliderImage.data:

				imageFile = save_image(imageForm=sliderForm.sliderImage.data,module=os.path.join("uploads","commerce","Slider"),id=slider.SlId)
				print(sliderForm.SlImgStartDate.data)
				image = Sl_image(
					SlImgName=imageFile['FileName'],
					SlImgDesc=sliderForm.sliderImageDesc.data,
					SlImgStartDate=dateDataCheck(sliderForm.SlImgStartDate.data),
					SlImgEndDate=dateDataCheck(sliderForm.SlImgEndDate.data),
					SlImgMainImgFileName=imageFile['FilePath'],				
					SlId=slider.SlId)
				db.session.add(image)
				db.session.commit()
				flash(lazy_gettext('Slider picture successfully uploaded!'),'success')
			return redirect(url_for('commerce_admin.slider_images',SlId=slider.SlId))
	else:
		return redirect(url_for('commerce_admin.sliders'))
	return render_template('commerce/admin/slider_setup.html',url_prefix=url_prefix,
		title=gettext('Sliders'),sliderForm=sliderForm,slider=slider,sl_images=sl_images)

@bp.route('/ui/svg-icons/',methods=['POST'])
@login_required
@ui_admin_required()
def ui_svg_icons():
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	icon_files = request.files.getlist('files[]')
	uploadedFiles=[]
	failedFiles=[]
	for icon_file in icon_files:
		if icon_file and allowed_icon(icon_file.filename):
			imageFile = save_icon(imageForm=icon_file,module=os.path.join("commerce","icons","categories","Others"),randomName=False)
			FileName = imageFile['FileName']
			FilePath = imageFile['FilePath']
			category = 'Others'
			iconInfo = {
				"url": url_for('commerce_api.get_icon',category=category,file_name=FileName),
				"icon_name": FileName,
				"category": category
			}
			uploadedFiles.append({
				"fileName": FileName,
				"htmlData": render_template('/commerce/admin/svgIconAppend.html',
					iconInfo=iconInfo),
			})
		else:
			failedFiles.append({
				"fileName": icon_file.fileName
			})

	response = jsonify({
		"data": uploadedFiles,
		"total": len(uploadedFiles),
		"failed": failedFiles,
		"failedTotal": len(failedFiles)
		})
	return response

@bp.route("/remove_svg_icon")
@login_required
@ui_admin_required()
def remove_svg_icon():
	try:
		name = request.args.get('name')
		icon_category = request.args.get('icon_category')
		path=os.path.join(current_app.root_path,'static',"commerce","icons","categories",icon_category,name)
		os.remove(path)
		flash("Image successfully deleted!",'success')
	except Exception as ex:
		print(ex)
		flash("Error, unable to execute this",'warning')
	return redirect(url_for('commerce_admin.category_table'))