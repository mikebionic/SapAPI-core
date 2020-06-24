from flask import session
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.base.apiMethods import fileToURL
from main_pack.models.base.models import Company
from main_pack.models.commerce.models import Res_category

from sqlalchemy import and_
from main_pack.models.base.models import Company,Sl_image,Slider,Image

from main_pack.base.languageMethods import dataLangSelector

def slidersData():
	slider = Slider.query.get(1)
	if slider:
		sl_images = Sl_image.query.filter(and_(Sl_image.SlId==slider.SlId, Sl_image.GCRecord==None)).all()
		List_FileName = [sl_image.SlImgName for sl_image in sl_images]
		print(List_FileName)
		imagesList = []
		for imageName in List_FileName:
			sliderImage = {}
			sliderImage['SlImgMainImgFilePathS']=fileToURL(fileType="slider",size='S',name=imageName) if List_FileName else ''
			sliderImage['SlImgMainImgFilePathM']=fileToURL(fileType="slider",size='M',name=imageName) if List_FileName else ''
			sliderImage['SlImgMainImgFilePathR']=fileToURL(fileType="slider",size='R',name=imageName) if List_FileName else ''
			imagesList.append(sliderImage)

		print(imagesList)
		res = {
			'sl_images':imagesList
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
	# res = {
	# 	"status":1,
	# 	"message":"All view categories",
	# 	"data":data,
	# 	"total":len(data)
	# }
	company = Company.query.get(1)

	logoIcon = {} 
	company_logo = Image.query.filter(and_(Image.CId==company.CId, Image.GCRecord==None))\
		.order_by(Image.CreatedDate.desc()).first()
	if company_logo:
		logoIcon["FilePathS"] = fileToURL(size='S',name=company_logo.FileName)
		logoIcon["FilePathM"] = fileToURL(size='M',name=company_logo.FileName)
		logoIcon["FilePathR"] = fileToURL(size='R',name=company_logo.FileName)

	res = {
		"categories":data,
		"company":company,
		"company_logo":logoIcon
	}
	return res


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
from main_pack.models.base.models import Company,Division,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####
from main_pack.models.base.models import Language
from main_pack.models.commerce.models import Color,Size,Brand

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


##### for realResRelatedData
from main_pack.models.commerce.models import Resource 
def realResRelatedData():
	resRelatedData = {}
	resources = Resource.query.all()
	barcodes = Barcode.query.all()
	resColors = Res_color.query.all()
	resSizes = Res_size.query.all()
	resTranslations = Res_translations.query.all()
	resUnits = Res_unit.query.all()
	resPrices = Res_price.query.all()
	resTotals = Res_total.query.all()
	resTransactions = Res_transaction.query.all()
	resDiscounts = Res_discount.query.all()

	images = Image.query.all()
	units = Unit.query.all()
	brands = Brand.query.all()
	usageStatuses = Usage_status.query.all()
	resCategories = Res_category.query.all()
	resTypes = Res_type.query.all()
	resMakers = Res_maker.query.all()
	rpAccs = Rp_acc.query.all()
	languages = Language.query.all()
	colors = Color.query.all()
	sizes = Size.query.all()
	brands = Brand.query.all()

	subcategory_children = []
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				pass
			else:
				subcategory_children.append(category)

	resRelatedData = {
		# 'resources':resources,
		'barcodes':barcodes,
		'resColors':resColors,
		'resSizes':resSizes,
		'resTranslations':resTranslations,
		'resUnits':resUnits,
		'resPrices':resPrices,
		'resTotals':resTotals,
		'resTransactions':resTransactions,
		'resDiscounts':resDiscounts,

		'images':images,
		'units':units,
		'brands':brands,
		'usageStatuses':usageStatuses,
		'resCategories':resCategories,
		'resTypes':resTypes,
		'resMakers':resMakers,
		'rpAccs':rpAccs,
		'languages':languages,
		'colors':colors,
		'sizes':sizes,
		'brands':brands,
		}

	return resRelatedData

##########

def UiResLimitedList(amount):
	resources = Resource.query\
		.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.CreatedDate.desc()).limit(amount).all()
	barcodes = Barcode.query\
		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
	res_prices = Res_price.query\
		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
	res_totals = Res_total.query\
		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

	res_colors = Res_color.query\
		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
	res_sizes = Res_size.query\
		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

	data = []
	for resource in resources:
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
		resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''

		resourceList["Colors"] = List_Colors if List_Colors else ''
		resourceList["Sizes"] = List_Sizes if List_Sizes else ''
		resourceList["Brand"] = List_Brands[0] if List_Brands else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}
	return res
###############

def UiResourcesList():
	resources = Resource.query\
		.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
	barcodes = Barcode.query\
		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
	res_prices = Res_price.query\
		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
	res_totals = Res_total.query\
		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

	res_colors = Res_color.query\
		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
	res_sizes = Res_size.query\
		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

	usage_statuses = Usage_status.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	units = Unit.query\
		.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()

	data = []
	for resource in resources:
		resourceList = resource.to_json_api()

		## one of these are usless
		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brand = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
		List_Unit = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]
		##  ##
		List_UsageStatus = [usage_status.to_json_api() for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
		
		resourceList["Colors"] = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		resourceList["Sizes"] = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		resourceList["Brand"] = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
		
		resourceList["UsageStatus"] = dataLangSelector(List_UsageStatus[0]) if List_UsageStatus else ''
		resourceList["Unit"] = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]
		
		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
		resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}
	return res

def UiPaginatedResList(product_list):
	barcodes = Barcode.query\
		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
	res_prices = Res_price.query\
		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
	res_totals = Res_total.query\
		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

	res_colors = Res_color.query\
		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
	res_sizes = Res_size.query\
		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

	data = []

	for product in product_list:
		resource = Resource.query.get(product["resId"])
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
		resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''

		resourceList["Colors"] = List_Colors if List_Colors else ''
		resourceList["Sizes"] = List_Sizes if List_Sizes else ''
		resourceList["Brand"] = List_Brands[0] if List_Brands else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}
	return res