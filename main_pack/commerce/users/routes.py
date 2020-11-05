from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack.commerce.users import bp
from main_pack.config import Config
import os
import uuid

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.languageMethods import dataLangSelector
from sqlalchemy import and_
# / useful methods /

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import UiCategoriesList
from main_pack.models.commerce.models import Resource,Wish
# / Resource and view /

# users and customers
from main_pack.models.users.models import Rp_acc
from main_pack.commerce.users.forms import UpdateProfileForm,UpdateRpAccForm
# / users and customers /

# Image operations
from main_pack.models.base.models import Image
from main_pack.base.imageMethods import save_image
from main_pack.base.apiMethods import fileToURL
# / Image operations /


@bp.route(Config.COMMERCE_PROFILE_PAGE)
@login_required
def profile():
	categoryData = UiCategoriesList()
	rpAcc = Rp_acc.query.filter_by(RpAccId = current_user.RpAccId).first()
	avatar = url_for('static', filename=f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/images/account-image-placeholder.png") 
	if rpAcc:
		image = Image.query\
			.filter_by(RpAccId = rpAcc.RpAccId)\
			.order_by(Image.CreatedDate.desc())\
			.first()
		if image:
			avatar = fileToURL(file_type='image',file_size='S',file_name=image.FileName)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/profile.html",**categoryData,
		rpAcc=rpAcc,avatar=avatar,title=gettext(Config.COMMERCE_PROFILE_PAGE_TITLE))

@bp.route(Config.COMMERCE_WISHLIST_PAGE)
@login_required
def wishlist():
	categoryData = UiCategoriesList()
	rpAcc = Rp_acc.query\
		.filter_by(RpAccId = current_user.RpAccId)\
		.first()

	page = request.args.get("page",1,type=int)
	pagination_wishes = Wish.query\
		.filter_by(GCRecord = None, RpAccId = rpAcc.RpAccId)\
		.order_by(Wish.CreatedDate.desc())\
		.paginate(per_page=Config.RESOURCES_PER_PAGE,page=page)
	product_list = []
	for wish in pagination_wishes.items:
		product = {}
		product['ResId'] = wish.ResId
		product_list.append(product)
	res = apiResourceInfo(product_list)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/wishlist.html",
		**categoryData,**res,pagination_url='commerce_users.wishlist',
		pagination_wishes=pagination_wishes,title=gettext(Config.COMMERCE_WISHLIST_PAGE_TITLE))

@bp.route(Config.COMMERCE_PROFILE_EDIT_PAGE,methods=['GET','POST'])
@login_required
def profile_edit():
	form = UpdateRpAccForm()
	rpAcc = Rp_acc.query\
		.filter_by(RpAccId = current_user.RpAccId)\
		.first()
	
	if form.validate_on_submit():
		userData = {
			'UName':form.username.data,
			'UFullName':form.fullname.data
		}
		current_user.update(**userData)

		rpAccData = {
			'RpAccUName':form.username.data,
			'RpAccName':form.fullname.data,
			'RpAccAddress':form.address.data,
			'RpAccMobilePhoneNumber':form.mobilePhone.data,
			'RpAccHomePhoneNumber':form.homePhone.data,
			'RpAccZipCode':form.zipCode.data,
			# 'RpAccEMail':form.email.data
		}
		rpAcc.update(**rpAccData)
		if form.picture.data:
			imageFile = save_image(
				imageForm = form.picture.data,
				module = os.path.join("uploads","commerce","Rp_acc"),
				id = rpAcc.RpAccId)
			lastImage = Image.query.order_by(Image.ImgId.desc()).first()
			ImgId = lastImage.ImgId+1
			image = Image(
				ImgId = ImgId,
				ImgGuid = uuid.uuid4(),
				FileName = imageFile['FileName'],
				FilePath = imageFile['FilePath'],
				RpAccId = rpAcc.RpAccId)
			db.session.add(image)

		db.session.commit()
		flash(lazy_gettext('Profile successfully updated!'), 'success')
		return redirect(url_for('commerce_users.profile'))
	
	
	form.username.data = rpAcc.RpAccUName
	form.fullname.data = rpAcc.RpAccName
	form.address.data = rpAcc.RpAccAddress
	form.mobilePhone.data = rpAcc.RpAccMobilePhoneNumber
	form.homePhone.data = rpAcc.RpAccHomePhoneNumber
	form.zipCode.data = rpAcc.RpAccZipCode

	image = Image.query\
		.filter_by(RpAccId = rpAcc.RpAccId)\
		.order_by(Image.CreatedDate.desc())\
		.first()
	if image:
		avatar = fileToURL(file_type='image',file_size='S',file_name=image.FileName)
	else:
		avatar = url_for('static', filename=f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/images/account-image-placeholder.png") 

	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/profile_edit.html",**categoryData,
		form=form,avatar=avatar,title=gettext(Config.COMMERCE_PROFILE_EDIT_PAGE_TITLE))