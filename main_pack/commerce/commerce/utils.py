from main_pack.config import Config
# auth and validation
from flask_login import current_user,login_required
# / auth and validation /
# useful methods
from main_pack import db,babel,gettext,lazy_gettext
from sqlalchemy import and_
from datetime import datetime
from main_pack.base.apiMethods import fileToURL
from main_pack.base.languageMethods import dataLangSelector
# / useful methods / 

# db Models
from main_pack.models.commerce.models import (Res_category,
																							Resource)
from main_pack.models.base.models import (Company,
																					Sl_image,
																					Slider,
																					Image)
# / db Models /
from main_pack.api.commerce.commerce_utils import UiCartResourceData

def slidersData():
	data = []
	sliders = Slider.query.filter_by(GCRecord = None).all()
	for slider in sliders:
		List_sliders = slider.to_json_api()
		sl_images = Sl_image.query\
			.filter_by(GCRecord = None, SlId = slider.SlId)\
			.all()
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
	categories = Res_category.query.filter_by(GCRecord = None).all()

	# categories = Res_category.query\
	# 	.filter_by(GCRecord = None)\
	# 	.join(Resource, Resource.ResCatId == Res_category.ResCatId)\
	# 	.filter(Resource.GCRecord == None)\
	# 	.join(Res_total, Res_total.ResId == Resource.ResId)\
	# 	.filter(and_(
	# 		Res_total.WhId == 1, 
	# 		Res_total.ResTotBalance > 0))\
	# 	.order_by(Res_category.ResCatVisibleIndex.asc())\
	# 	.all()

	category_info = [category.to_json_api() for category in categories if categories]
	categories = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == 0 or category_data["ResOwnerCatId"] == None]
	for category in categories:
		subcategories = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == category["ResCatId"]]
		for subcategory in subcategories:
			subcategory_children = [category_info[category_info.index(category_data)] for category_data in category_info if category_data["ResOwnerCatId"] == subcategory["ResCatId"]]
			subcategory["Categories"] = subcategory_children
		category["Categories"] = subcategories

	company = Company.query.get(1)
	logoIcon = {}
	company_logo = Image.query\
		.filter_by(GCRecord = None, CId = company.CId)\
		.order_by(Image.CreatedDate.desc())\
		.first()
	if company_logo:
		logoIcon["FilePath"] = fileToURL(file_type='image',file_name=company_logo.FileName)
	res = {
		"categories": categories,
		"company": company,
		"company_logo": logoIcon
	}
	return res

def UiBrandsList():
	brands = Brand.query.filter_by(GCRecord = None).all() 
	data = []
	for brand in brands:
		brand_info = brand.to_json_api()
		List_Images = [image.to_json_api() for image in brand.Image if image.GCRecord == None]
		brand_info['Images'] = List_Images if List_Images else []
		brand_info["FilePath"] = fileToURL(file_type='image',file_name=List_Images[-1]['FileName']) if List_Images else ''
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
	units = Unit.query\
		.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()
	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()
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