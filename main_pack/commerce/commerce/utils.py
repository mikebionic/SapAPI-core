from flask import session
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.apiMethods import fileToURL
from main_pack.models.base.models import Company
from main_pack.models.commerce.models import Res_category

from sqlalchemy import and_
from main_pack.models.base.models import Company,Sl_image,Slider,Image
from main_pack.base.languageMethods import dataLangSelector
from datetime import datetime

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
	print(res)
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
		"categories":data,
		"company":company,
		"company_logo":logoIcon
	}
	return res

# categories, company info {not used}
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
		"categories":categories,
		"subcategories":subcategories,
		"subcategory_children":subcategory_children,
		"company":company
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















# def UiResLimitedList(amount):
# 	resources = Resource.query\
# 		.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
# 		.order_by(Resource.CreatedDate.desc()).limit(amount).all()
# 	barcodes = Barcode.query\
# 		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
# 	categories = Res_category.query\
# 		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
# 	res_prices = Res_price.query\
# 		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
# 	res_totals = Res_total.query\
# 		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
# 	images = Image.query\
# 		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

# 	colors = Color.query\
# 		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
# 	sizes = Size.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	brands = Brand.query\
# 		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

# 	res_colors = Res_color.query\
# 		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
# 	res_sizes = Res_size.query\
# 		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

# 	data = []
# 	for resource in resources:
# 		resourceList = resource.to_json_api()

# 		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
# 		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
# 		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
# 		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
# 		List_Images = [image.to_json_api() for image in images if image.ResId==resource.ResId]

# 		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
# 		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
# 		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

# 		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
# 		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
# 		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
# 		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
# 		resourceList["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''

# 		resourceList["Colors"] = List_Colors if List_Colors else ''
# 		resourceList["Sizes"] = List_Sizes if List_Sizes else ''
# 		resourceList["Brand"] = List_Brands[0] if List_Brands else ''

# 		data.append(resourceList)
# 	res = {
# 		"status":1,
# 		"message":"All view resources",
# 		"data":data,
# 		"total":len(data)
# 	}
# 	return res
# ###############












# def apiResourceInfo(resource_list):
# 	barcodes = Barcode.query\
# 		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
# 	categories = Res_category.query\
# 		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
# 	res_prices = Res_price.query\
# 		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
# 	res_totals = Res_total.query\
# 		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
# 	images = Image.query\
# 		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()
# 	colors = Color.query\
# 		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
# 	sizes = Size.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	brands = Brand.query\
# 		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

# 	res_colors = Res_color.query\
# 		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
# 	res_sizes = Res_size.query\
# 		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()
# 	usage_statuses = Usage_status.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	units = Unit.query\
# 		.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()
# 	data = []
# 	fails = []
# 	for product in resource_list:
# 		resource = Resource.query\
# 			.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
# 				Resource.ResId==product["ResId"]).first()
# 		try:
# 			resourceList = resource.to_json_api()
# 			List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
# 			List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
# 			List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
# 			List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
# 			List_Images = [image.to_json_api() for image in images if image.ResId==resource.ResId]

# 			List_Colors = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
# 			List_Sizes = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
# 			List_Brands = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
# 			List_Usage_statuses = [usage_status.UsageStatusName_tkTM for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
# 			List_Units = [unit.UnitName_tkTM for unit in units if unit.UnitId==resource.UnitId]

# 			resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
# 			resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
# 			resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
# 			resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
# 			resourceList["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
# 			resourceList["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
# 			resourceList["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''
# 			resourceList["Images"] = List_Images if List_Images else []
# 			resourceList["Colors"] = List_Colors if List_Colors else []
# 			resourceList["Sizes"] = List_Sizes if List_Sizes else []
# 			resourceList["Brand"] = List_Brands[0] if List_Brands else ''
# 			resourceList["Unit"] = List_Units[0] if List_Units else ''
# 			resourceList["UsageStatus"] = List_Usage_statuses[0] if List_Usage_statuses else ''
				
# 			data.append(resourceList)
# 		except:
# 			fails.append(product)
			
# 	status = checkApiResponseStatus(data,fails)
# 	if len(data)==1:
# 		data = data[0]
# 	if len(fails)==1:
# 		fails = fails[0]
# 	res = {
# 			"message":"Resources",
# 			"data":data,
# 			"fails":fails,
# 			"total":len(data),
# 			"fail_total":len(fails)
# 	}
# 	for e in status:
# 		res[e]=status[e]
# 	response = make_response(jsonify(res),200)
# 	return res






# def UiResourcesList():
# 	resources = Resource.query\
# 		.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
# 	barcodes = Barcode.query\
# 		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
# 	categories = Res_category.query\
# 		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
# 	res_prices = Res_price.query\
# 		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
# 	res_totals = Res_total.query\
# 		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
# 	images = Image.query\
# 		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

# 	colors = Color.query\
# 		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
# 	sizes = Size.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	brands = Brand.query\
# 		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

# 	res_colors = Res_color.query\
# 		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
# 	res_sizes = Res_size.query\
# 		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()


# 	data = []
# 	for resource in resources:
# 		resourceList = resource.to_json_api()

# 		## one of these are usless
# 		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
# 		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
# 		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
# 		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
# 		List_Images = [image.to_json_api() for image in images if image.ResId==resource.ResId]

# 		List_Colors = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
# 		List_Sizes = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
# 		List_Brand = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
# 		##  ##

# 		resourceList["Colors"] = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
# 		resourceList["Sizes"] = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
# 		resourceList["Brand"] = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]


# 		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
# 		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
# 		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
# 		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
# 		resourceList["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''

# 		data.append(resourceList)
# 	res = {
# 		"status":1,
# 		"message":"All view resources",
# 		"data":data,
# 		"total":len(data)
# 	}
# 	return res

# def UiPaginatedResList(product_list):
# 	barcodes = Barcode.query\
# 		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
# 	categories = Res_category.query\
# 		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
# 	res_prices = Res_price.query\
# 		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
# 	res_totals = Res_total.query\
# 		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
# 	images = Image.query\
# 		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()
# 	colors = Color.query\
# 		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
# 	sizes = Size.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	brands = Brand.query\
# 		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

# 	res_colors = Res_color.query\
# 		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
# 	res_sizes = Res_size.query\
# 		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()
# 	usage_statuses = Usage_status.query\
# 		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
# 	units = Unit.query\
# 		.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()

# 	data = []

# 	for product in product_list:
# 		resource = Resource.query.get(product["resId"])
# 		resourceList = resource.to_json_api()

# 		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
# 		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
# 		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
# 		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
# 		List_Images = [image.to_json_api() for image in images if image.ResId==resource.ResId]
# 		List_UsageStatus = [usage_status.to_json_api() for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
# 		List_Unit = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]

# 		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
# 		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
# 		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

# 		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
# 		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
# 		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
# 		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
# 		resourceList["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
# 		resourceList["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''

# 		resourceList["Colors"] = List_Colors if List_Colors else ''
# 		resourceList["Sizes"] = List_Sizes if List_Sizes else ''
# 		resourceList["Brand"] = List_Brands[0] if List_Brands else ''
# 		resourceList["UsageStatus"] = dataLangSelector(List_UsageStatus[0]) if List_UsageStatus else ''
# 		resourceList["Unit"] = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]

# 		data.append(resourceList)
# 	res = {
# 		"status":1,
# 		"message":"All view resources",
# 		"data":data,
# 		"total":len(data)
# 	}
# 	return res
