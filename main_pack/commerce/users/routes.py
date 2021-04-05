from flask import render_template, url_for, session, flash, redirect, request 
import os
import uuid
from datetime import datetime
from flask_login import current_user,login_required
from sqlalchemy import and_

from . import bp, url_prefix
from main_pack.config import Config
from main_pack import db, gettext, lazy_gettext

# Resource and view
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.commerce.commerce.utils import UiCategoriesList
from main_pack.models import Resource,Wish
# / Resource and view /

# users and customers
from main_pack.models import Rp_acc
from main_pack.commerce.users.forms import UpdateRpAccForm
# / users and customers /

# Image operations
from main_pack.models import Image
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
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/profile.html",
		**categoryData,
		rpAcc = rpAcc,
		avatar = avatar,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_PROFILE_PAGE_TITLE))


@bp.route(Config.COMMERCE_WISHLIST_PAGE)
@login_required
def wishlist():
	categoryData = UiCategoriesList()

	page = request.args.get("page",1,type=int)
	pagination_wishes = Wish.query\
		.filter_by(GCRecord = None, RpAccId = current_user.RpAccId)\
		.order_by(Wish.CreatedDate.desc())\
		.paginate(per_page = Config.RESOURCES_PER_PAGE, page = page)

	product_list = []
	for wish in pagination_wishes.items:
		product = {}
		product['ResId'] = wish.ResId
		product_list.append(product)

	res = apiResourceInfo(product_list)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/wishlist.html",
		**categoryData,
		**res,
		pagination_url = 'commerce_users.wishlist',
		pagination_wishes = pagination_wishes,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_WISHLIST_PAGE_TITLE))


@bp.route(Config.COMMERCE_PROFILE_EDIT_PAGE,methods=['GET','POST'])
@login_required
def profile_edit():
	form = UpdateRpAccForm()

	rpAcc = Rp_acc.query\
		.filter_by(RpAccId = current_user.RpAccId)\
		.first()
	
	if form.validate_on_submit():
		rpAccData = {
			"RpAccUName": form.username.data,
			"RpAccName": form.fullname.data,
			"RpAccAddress": form.address.data,
			"RpAccMobilePhoneNumber": form.mobilePhone.data,
			"RpAccHomePhoneNumber": form.homePhone.data,
			"RpAccZipCode": form.zipCode.data,
			# 'RpAccEMail':form.email.data
		}

		try:
			current_user.update(**rpAccData)

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

		except Exception as ex:
			print(f"{datetime.now()} | Profile edit error {ex}")
			flash(lazy_gettext('Unknown error!'), 'warning')

		return redirect(url_for('commerce_users.profile'))
	
	
	form.username.data = current_user.RpAccUName
	form.fullname.data = current_user.RpAccName
	form.address.data = current_user.RpAccAddress
	form.mobilePhone.data = current_user.RpAccMobilePhoneNumber
	form.homePhone.data = current_user.RpAccHomePhoneNumber
	form.zipCode.data = current_user.RpAccZipCode

	image = Image.query\
		.filter_by(RpAccId = current_user.RpAccId, GCRecord = None)\
		.order_by(Image.CreatedDate.desc())\
		.first()

	if image:
		avatar = fileToURL(file_type='image', file_size='S', file_name=image.FileName)
	else:
		avatar = url_for('static', filename=f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/images/account-image-placeholder.png") 

	categoryData = UiCategoriesList()
	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/users/profile_edit.html",
		**categoryData,
		form = form,
		avatar = avatar,
		url_prefix = url_prefix,
		title = gettext(Config.COMMERCE_PROFILE_EDIT_PAGE_TITLE))