from main_pack.config import Config
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from datetime import datetime

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# db Models
from main_pack.models.commerce.models import (
	Res_category,
	Resource)
from main_pack.models.base.models import (
	Company,
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


def slidersData():
	data = []
	sliders = Slider.query\
		.filter_by(GCRecord = None)\
		.options(joinedload(Slider.Sl_image))\
		.filter(Sl_image.GCRecord == None)\
		.all()
	for slider in sliders:
		List_sliders = slider.to_json_api()
		sl_images = slider.Sl_image
		List_sl_images = []
		for sl_image in sl_images:
			if sl_image.SlImgEndDate:
				if (sl_image.SlImgStartDate <= datetime.now()):
					if (sl_image.SlImgEndDate and sl_image.SlImgEndDate>datetime.now()):
						List_sl_images.append(sl_image.to_json_api())
			else:
				List_sl_images.append(sl_image.to_json_api())
		List_sliders['Sl_images'] = List_sl_images

		data.append(List_sliders)
	res = {
		'sliders':data
	}
	return res

def UiCategoriesList():
	categories = collect_categories_query()

	category_info = [category.to_json_api() for category in categories if categories]
	categories = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == 0 or category_data["ResOwnerCatId"] == None]
	for category in categories:
		subcategories = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == category["ResCatId"]]
		for subcategory in subcategories:
			subcategory_children = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == subcategory["ResCatId"]]
			subcategory["Categories"] = subcategory_children
		category["Categories"] = subcategories

	company = Company.query\
		.filter_by(GCRecord = None)\
		.options(joinedload(Company.Image))\
		.filter(Image.GCRecord == None)\
		.order_by(Image.CreatedDate.desc())\
		.first()
	logoIcon = {}
	company_logos = company.Image
	if company_logos:
		logoIcon["FilePath"] = fileToURL(file_type='image',file_name=company_logos[0].FileName)
	res = {
		"categories": categories,
		"company": company,
		"company_logo": logoIcon
	}
	return res

def UiBrandsList():
	brands = Brand.query\
		.filter_by(GCRecord = None)\
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
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division
from main_pack.models.users.models import Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####
from main_pack.models.base.models import Language
from main_pack.models.commerce.models import Color,Size,Brand
from main_pack.models.commerce.models import Resource

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
	recipient = Config.MAIL_USERNAME
	msg = Message('Message from users',
		sender = "noterply@mail.io",
		recipients = [recipient])
	msg.body = message
	mail.send(msg)