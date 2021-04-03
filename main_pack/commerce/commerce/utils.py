from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from datetime import datetime

from flask_login import current_user, login_required
from main_pack.config import Config
from main_pack import cache

# db Models
from main_pack.models import (
	Res_category,
	Resource)
from main_pack.models import (
	Company,
	Division,
	Sl_image,
	Slider,
	Image)
# / db Models /

# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.apiMethods import fileToURL
from main_pack.base.languageMethods import dataLangSelector
from main_pack.api.commerce.commerce_utils import UiCartResourceData
from main_pack.api.commerce.commerce_utils import collect_categories_query
# / useful methods /


@cache.cached(Config.DB_CACHE_TIME, key_prefix="ui_sliders")
def slidersData():
	data = []
	sliders = Slider.query\
		.filter_by(GCRecord = None)\
		.options(joinedload(Slider.Sl_image))\
		.all()

	for slider in sliders:
		List_sliders = slider.to_json_api()

		List_sl_images = []

		for sl_image in slider.Sl_image:
			if not sl_image.GCRecord:

				if sl_image.SlImgEndDate:
					if (sl_image.SlImgStartDate <= datetime.now()):
						if (sl_image.SlImgEndDate and sl_image.SlImgEndDate > datetime.now()):
							List_sl_images.append(sl_image.to_json_api())

				else:
					List_sl_images.append(sl_image.to_json_api())

		List_sliders['Sl_images'] = List_sl_images

		data.append(List_sliders)

	res = {'sliders': data}
	return res


@cache.cached(Config.DB_CACHE_TIME, key_prefix="ui_categories")
def UiCategoriesList():

	categories = collect_categories_query(
		showNullResourceCategory = Config.SHOW_NULL_RESOURCE_CATEGORY,
	)\
	.options(joinedload(Res_category.Resource))\
	.all()

	main_categories = []
	last_categories = []
	for category in categories:
		if not category.ResOwnerCatId:
			if (category.ResCatVisibleIndex > 0):
				main_categories.append(category)
			else:
				last_categories.append(category)

	if last_categories:
		for category in last_categories:
			main_categories.append(category)

	categories_list = []

	for main_category in main_categories:
		subcategories = [category for category in main_category.subcategory if not category.GCRecord]

		data = []
		for subcategory in subcategories:
			category_data = subcategory.to_json_api()
			subcategory_children = [category.to_json_api() for category in subcategory.subcategory if not category.GCRecord]
			category_data["Categories"] = subcategory_children
			data.append(category_data)

		category_data = main_category.to_json_api()
		category_data["Categories"] = data
		categories_list.append(category_data)

	company = Company.query\
		.filter_by(GCRecord = None)\
		.options(joinedload(Company.Image))\
		.filter(Image.GCRecord == None)\
		.order_by(Image.CreatedDate.desc())\
		.first()

	logoIcon = {}
	if company:
		if company.Image:
			logoIcon["FilePath"] = fileToURL(file_type='image',file_name=company.Image[0].FileName)

	res = {
		"categories": categories_list,
		"company": company,
		"company_logo": logoIcon
	}
	return res


@cache.cached(Config.DB_CACHE_TIME, key_prefix="ui_brands")
def UiBrandsList():
	brands = Brand.query\
		.filter_by(GCRecord = None)\
		.order_by(Brand.BrandVisibleIndex.asc())\
		.options(joinedload(Brand.Image))\
		.filter(Image.GCRecord == None)\
		.order_by(Image.CreatedDate.desc())\
		.all()
	data = []
	for brand in brands:
		brand_info = brand.to_json_api()
		List_Images = [image.to_json_api() for image in brand.Image if brand.Image]
		brand_info['Images'] = List_Images if List_Images else []
		brand_info["FilePath"] = fileToURL(file_type='image',file_name=List_Images[0]['FileName']) if List_Images else ''
		data.append(brand_info)
	res = {
		"message": "Brands",
		"data": data,
		"total": len(data)
	}
	return res


# used foreign keys
from main_pack.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models import Company,Division
from main_pack.models import Rp_acc
####
# used relationship
from main_pack.models import (Barcode,Res_color,Res_size,Res_translation,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models import Image
#####
from main_pack.models import Language
from main_pack.models import Color,Size,Brand
from main_pack.models import Resource

def uiSortingData():
	uiSortingData = {}
	units = Unit.query.filter_by(GCRecord = None).all()
	brands = Brand.query.filter_by(GCRecord = None).all()
	colors = Color.query.filter_by(GCRecord = None).all()
	sizes = Size.query.filter_by(GCRecord = None).all()
	brands = Brand.query.filter_by(GCRecord = None).all()
	uiSortingData = {
		'units':units,
		'colors':colors,
		'sizes':sizes,
		'brands':brands,
		}
	return uiSortingData


from main_pack import mail
from flask_mail import Message

def send_email_to_company(message):
	recipient = Config.COMPANY_MAIL
	msg = Message('Message from users',
		sender = Config.MAIL_USERNAME,
		recipients = [recipient])
	msg.body = message
	mail.send(msg)
	# !!! TODO: catch errors here
	return True