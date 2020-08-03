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
	sliders = Slider.query\
		.filter(Slider.GCRecord=='' or Slider.GCRecord==None).all()
	for slider in sliders:
		List_sliders = slider.to_json_api()
		sl_images = Sl_image.query.filter(and_(Sl_image.SlId==slider.SlId, Sl_image.GCRecord==None)).all()
		List_sl_images = []
		for sl_image in sl_images:
			if (sl_image.SlImgStartDate<=datetime.now()):
				if (sl_image.SlImgEndDate and sl_image.SlImgEndDate>datetime.now()):
					List_sl_images.append(sl_image.to_json_api())
		List_sliders['Sl_images'] = List_sl_images

		data.append(List_sliders)
	res = {
		'sliders':data
	}
	return res

def UiCategoriesList():
	data = []
	categories = Res_category.query\
		.filter(and_(Res_category.GCRecord=='' or Res_category.GCRecord==None),\
			(Res_category.ResOwnerCatId==0)).all()
	for category in categories:
		categoryPack = category.to_json_api()
		subcategories = Res_category.query\
			.filter(and_(Res_category.GCRecord=='' or Res_category.GCRecord==None),\
			(Res_category.ResOwnerCatId==category.ResCatId)).all()

		subcategory_List = []
		for subcategory in subcategories:
			subcategoryPack = subcategory.to_json_api()
			subcategory_children = Res_category.query\
				.filter(and_(Res_category.GCRecord=='' or Res_category.GCRecord==None),\
				(Res_category.ResOwnerCatId==subcategory.ResCatId)).all()

			children_List = []
			for child in subcategory_children:
				subcategoryChildPack = child.to_json_api()
				children_List.append(subcategoryChildPack)

			subcategoryPack['subcategories'] = children_List
			subcategory_List.append(subcategoryPack)
		categoryPack['subcategories'] = subcategory_List
		data.append(categoryPack)
	company = Company.query.get(1)

	logoIcon = {}
	company_logo = Image.query.filter(and_(Image.CId==company.CId, Image.GCRecord==None))\
		.order_by(Image.CreatedDate.desc()).first()
	if company_logo:
		logoIcon["FilePath"] = fileToURL(file_type='image',file_name=company_logo.FileName)

	res = {
		"categories": data,
		"company": company,
		"company_logo": logoIcon
	}
	return res

# categories, company info {not used} 
# !!! delete after reconfiguring navbar.html
def commonUsedData():
	commonData = {}
	subcategories = []
	subcategory_children = []
	company = Company.query.get(1)
	categories = Res_category.query.filter_by(ResOwnerCatId=0)
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				subcategories.append(category)
			else:
				subcategory_children.append(category)

	commonData.update({
		"categories": categories,
		"subcategories": subcategories,
		"subcategory_children": subcategory_children,
		"company": company
		})
	return commonData


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