from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response
from main_pack.config import Config
from main_pack.commerce.admin import bp, url_prefix
from main_pack import db, gettext, lazy_gettext, cache
from flask import current_app

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

# data operations
from main_pack.base.imageMethods import save_image,save_icon,allowed_icon,allowed_image
from main_pack.base.dataMethods import dateDataCheck
from main_pack.api.commerce.image_api import remove_image
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
# / data operations /

# data and models
from main_pack.models import Company,Sl_image,Slider,Image
from main_pack.models import Resource, Brand
from main_pack.api.commerce.commerce_utils import apiResourceInfo
import os
import uuid
# / data and models /

from main_pack.commerce.admin.forms import LogoImageForm,SliderImageForm,ResourceEditForm


@bp.route("/admin/logo_setup", methods=['GET', 'POST'])
@login_required
@ui_admin_required
def logo_setup():
	company = Company.query.filter_by(GCRecord = None).first()
	company_logo = Image.query\
		.filter_by(GCRecord = None, CId = company.CId)\
		.order_by(Image.CreatedDate.desc()).first()
	logoForm = LogoImageForm()

	if "logoForm" in request.form and logoForm.validate_on_submit():
		if logoForm.logoImage.data:
			imageFile = save_icon(imageForm=logoForm.logoImage.data,module=os.path.join("uploads","commerce","Company"),id=company.CId)
			
			lastImage = Image.query.order_by(Image.ImgId.desc()).first()
			ImgId = lastImage.ImgId+1
			image = Image(
				ImgId = ImgId,
				ImgGuid = uuid.uuid4(),
				FileName = imageFile['FileName'],
				FilePath = imageFile['FilePath'],
				CId = company.CId)
			db.session.add(image)
			db.session.commit()
			cache.clear()

		flash(lazy_gettext('Company logo successfully uploaded!'), 'success')
		return redirect(url_for('commerce_admin.logo_setup'))
	return render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/logo_setup.html",url_prefix=url_prefix,
		title=gettext('Company logo'),logoForm=logoForm,company_logo=company_logo)


@bp.route("/remove_images")
@login_required
@ui_admin_required
def remove_images():
	try:
		ImgId = request.args.get("imgId")
		ResId = request.args.get("prodId",None)
		imgType = request.args.get("type")

		url = url_for('commerce_admin.dashboard')

		if imgType == 'image' or imgType == 'icon':
			image = Image.query.get(ImgId)

			try:
				file_type = imgType
				file_name = image.FileName
				remove_image(file_type,file_name)
				db.session.delete(image)
			except Exception as ex:
				print(ex)
				image.GCRecord = 1

			db.session.commit()
			cache.clear()

			url = url_for('commerce_admin.logo_setup')
			if ResId:
				url = url_for('commerce_admin.resource_edit',ResId=ResId)

		elif imgType == 'slider':
			sl_image = Sl_image.query.get(ImgId)

			try:
				file_type = imgType
				file_name = Sl_image.SlImgMainImgFileName
				remove_image(file_type,file_name)
				db.session.delete(sl_image)

			except Exception as ex:
				sl_image.GCRecord = 1

			db.session.commit()
			cache.clear()

			url = url_for('commerce_admin.sliders')

		flash("Image successfully deleted!",'success')
	except Exception as ex:
		flash("Error, unable to execute this",'warning')

	return redirect(url)


@bp.route("/admin/sliders", methods=['GET', 'POST'])
@login_required
@ui_admin_required
def sliders():
	# handler for commerce view
	header_slider = Slider.query\
		.filter_by(GCRecord = None, SlName = 'commerce_header')\
		.options(joinedload(Slider.Sl_image))\
		.first()
	if header_slider is None:
		# create a commerce_header for header slider automatically
		slider = Slider(SlName="commerce_header")
		db.session.add(slider)
		db.session.commit()
		cache.clear()

	sliders = Slider.query\
		.filter_by(GCRecord = None)\
		.options(joinedload(Slider.Sl_image))\
		.all()
	slidersData = []
	for slider in sliders:
		sliderList = slider.to_json_api()

		sl_images = Sl_image.query\
			.filter_by(GCRecord = None,SlId = slider.SlId)\
			.all()
		
		slider_images = []
		for sl_image in sl_images:
			slider_images.append(sl_image.to_json_api())

		sliderList["Sl_images"] = slider_images
		slidersData.append(sliderList)

	return render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/sliders.html",url_prefix=url_prefix,
		title=gettext('Sliders'),sliders=slidersData)


@bp.route("/admin/sliders/<SlId>", methods=['GET', 'POST'])
@login_required
@ui_admin_required
def slider_images(SlId):
	slider = Slider.query\
		.filter_by(GCRecord = None, SlId = SlId)\
		.options(joinedload(Slider.Sl_image))\
		.first()
	if slider:
		sl_images = Sl_image.query\
			.filter_by(GCRecord = None, SlId = slider.SlId)\
			.all()
		sliderForm = SliderImageForm()

		if "sliderForm" in request.form and sliderForm.validate_on_submit():
			if sliderForm.sliderImage.data:

				imageFile = save_image(
					imageForm = sliderForm.sliderImage.data,
					module = os.path.join("uploads","commerce","Slider"),
					id = slider.SlId)

				image = Sl_image(
					SlImgMainImgFileName = imageFile['FileName'],
					SlImgTitle = sliderForm.sliderImageTitle.data,
					SlImgDesc = sliderForm.sliderImageDesc.data,
					SlImgLink = sliderForm.sliderLink.data,
					SlImgStartDate = dateDataCheck(sliderForm.SlImgStartDate.data),
					SlImgEndDate = dateDataCheck(sliderForm.SlImgEndDate.data),
					SlImgMainImgFilePath = imageFile['FilePath'],				
					SlId = slider.SlId)

				db.session.add(image)
				db.session.commit()
				cache.clear()

				flash(lazy_gettext('Slider picture successfully uploaded!'),'success')

			return redirect(url_for('commerce_admin.slider_images',SlId=slider.SlId))

	else:
		return redirect(url_for('commerce_admin.sliders'))

	return render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/slider_setup.html",url_prefix=url_prefix,
		title=gettext('Sliders'),sliderForm=sliderForm,slider=slider,sl_images=sl_images)


@bp.route('/ui/svg-icons/',methods=['POST'])
@login_required
@ui_admin_required
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
			imageFile = save_icon(
				imageForm = icon_file,
				module = os.path.join("commerce","icons","categories","Others"),
				randomName = False)
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
				"htmlData": render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/svgIconAppend.html",
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
@ui_admin_required
def remove_svg_icon():
	try:
		name = request.args.get("name")
		icon_category = request.args.get("icon_category")
		path=os.path.join(current_app.root_path,'static',"commerce","icons","categories",icon_category,name)
		os.remove(path)
		flash("Image successfully deleted!",'success')
	except Exception as ex:
		print(ex)
		flash("Error, unable to execute this",'warning')
	return redirect(url_for('commerce_admin.category_table'))

def brands():
	brands = Brand.query.filter_by(GCRecord = None).all()
	brands_list = [brand.to_json_api() for brand in brands]
	return brands_list


@bp.route("/admin/resource_edit/<ResId>", methods=['GET', 'POST'])
@login_required
@ui_admin_required
def resource_edit(ResId):
	resource = Resource.query\
		.filter_by(GCRecord = None, ResId = ResId)\
		.first()

	if not resource:
		return redirect(url_for('commerce_admin.resources_table'))
	
	res = apiResourceInfo(
		resource_list = [{"ResId": resource.ResId}],
		single_object = True,
		showInactive = True,
		avoidQtyCheckup = True)

	resource_info = res['data']
	resourceForm = ResourceEditForm()
	
	brands_list = brands()
	No_brand = (0,"...")
	brandChoices = [No_brand]
	for brand in brands_list:
		obj = (brand['BrandId'],brand['BrandName'])
		brandChoices.append(obj)
	
	if resource_info["BrandId"]:
		# try:
		BrandId = resource_info["BrandId"]
		BrandName = resource_info["BrandName"]
		brandChoices.insert(0, brandChoices.pop(brandChoices.index((BrandId,BrandName))))
		# except Exception as ex:
		# 	print(ex)

	resourceForm.BrandId.choices = brandChoices

	if "resourceForm" in request.form and resourceForm.validate_on_submit():
		resource.ResName = resourceForm.ResName.data
		resource.ResDesc = resourceForm.ResDesc.data
		resource.ResFullDesc = resourceForm.ResFullDesc.data
		resource.BrandId = resourceForm.BrandId.data if resourceForm.BrandId.data > 0 else None

		if resourceForm.resourceImage.data:
			imageFile = save_image(
				imageForm = resourceForm.resourceImage.data,
				module = os.path.join("uploads","commerce","Resource"),
				id = ResId,
				apply_watermark = True)

			lastImage = Image.query.order_by(Image.ImgId.desc()).first()
			ImgId = lastImage.ImgId + 1
			image = Image(
				ImgId = ImgId,
				ImgGuid = uuid.uuid4(),
				FileName = imageFile['FileName'],
				FilePath = imageFile['FilePath'],
				ResId = ResId)
			db.session.add(image)
			db.session.commit()

			flash("{} {}".format(lazy_gettext('Resource picture'), lazy_gettext('successfully uploaded!')),'success')

		db.session.commit()
		cache.clear()

		return redirect(url_for('commerce_admin.resource_edit',ResId=ResId))

	resourceForm.ResName.data = resource_info["ResName"]
	resourceForm.ResDesc.data = resource_info["ResDesc"]
	resourceForm.ResFullDesc.data = resource_info["ResFullDesc"]
	
	resourceForm.BrandId.choices = brandChoices

	return render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/resource_edit.html",url_prefix=url_prefix,
		title=resource_info["ResName"],resourceForm=resourceForm,resource=resource_info)