# used foreign keys
from main_pack.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models import Company,Division
from main_pack.models import Rp_acc
####
# used relationship
from main_pack.models import (
	Barcode,
	Res_color,
	Res_size,
	Res_translation,
	Unit,
	Res_unit,
	Inv_line,
	Inv_line_det,
	Order_inv_line,
	Res_price,
	Res_total,
	Res_trans_inv_line,
	Res_transaction,
	Rp_acc_resource,
	Sale_agr_res_price,
	Res_discount)

from main_pack.models import Image
#####
from main_pack.models import Language
from main_pack.models import Color,Size,Brand

def resRelatedData():
	resRelatedData = {}
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
		"units": units,
		"brands": brands,
		"usageStatuses": usageStatuses,
		"resCategories": resCategories,
		"resTypes": resTypes,
		"resMakers": resMakers,
		"rpAccs": rpAccs,
		"languages": languages,
		"colors": colors,
		"sizes": sizes,
		"brands": brands,
		"subcategory_children": subcategory_children,
		}

	return resRelatedData

########### to dict methods ########

def addSliderDict(req):
	SlId = req.get('sliderId')
	CId = req.get('companyId')
	DivId = req.get('divisionId')
	SlName = req.get('sliderName')
	SlDesc = req.get('sliderDesc')
	slider = {
		"CId": CId,
		"DivId": DivId,
		"SlName": SlName,
		"SlDesc": SlDesc,
	}
	if(SlId != '' and SlId != None):
		slider['SlId']=SlId
	slider=configureNulls(slider)
	return slider

	# slider_forms = ['sliderId','companyId','divisionId','sliderName','sliderDesc']

def addSliderImageDict(req):
	SlImgId = req.get('sliderImgId')
	SlId = req.get('sliderId')
	SlImgTitle = req.get('sliderImgTitle')
	SlImgDesc = req.get('sliderImgDesc')
	SlImgMainImgFileName = req.get('sliderImgName')
	SlImgMainImgFilePath = req.get('sliderImgMainImgFileName')
	SlImgSubImageFileName1 = req.get('sliderImgSubImageFileName1')
	SlImgSubImageFileName2 = req.get('sliderImgSubImageFileName2')
	SlImgSubImageFileName3 = req.get('sliderImgSubImageFileName3')
	SlImgSubImageFileName4 = req.get('sliderImgSubImageFileName4')
	SlImgSubImageFileName5 = req.get('sliderImgSubImageFileName5')
	SlImgStartDate = req.get('sliderImgStartDate')
	SlImgEndDate = req.get('sliderImgEndDate')

	slider_image = {
		"SlId": self.SlId,
		"SlImgTitle": self.SlImgTitle,
		"SlImgDesc": self.SlImgDesc,
		"SlImgMainImgFileName": self.SlImgMainImgFileName,
		"SlImgMainImgFilePath": self.SlImgMainImgFilePath,
		"SlImgSubImageFileName1": self.SlImgSubImageFileName1,
		"SlImgSubImageFileName2": self.SlImgSubImageFileName2,
		"SlImgSubImageFileName3": self.SlImgSubImageFileName3,
		"SlImgSubImageFileName4": self.SlImgSubImageFileName4,
		"SlImgSubImageFileName5": self.SlImgSubImageFileName5,
		"SlImgStartDate": self.SlImgStartDate,
		"SlImgEndDate": self.SlImgEndDate,
	}
	if(SlImgId != '' and SlImgId != None):
		slider_image['SlImgId']=SlImgId
	slider_image=configureNulls(slider_image)
	return slider_image

# sider_image_forms = ['sliderImgId','sliderId','sliderImgName','sliderImgDesc',
# 	'sliderImgMainImgFileName','sliderImgSubImageFileName1','sliderImgSubImageFileName2',
# 	'sliderImgSubImageFileName3','sliderImgSubImageFileName4','sliderImgSubImageFileName5',
# 	'sliderImgStartDate','sliderImgEndDate']


def addCategoryDict(req):
	ResCatId = req.get('categoryId')
	ResOwnerCatId = req.get('categoryOwner')
	ResCatVisibleIndex = req.get('visibleIndex')
	IsMain = req.get('isMain')
	ResCatName = req.get('categoryName')
	ResCatDesc = req.get('categoryDesc')
	ResCatIconName = req.get('categoryIcon')
	ResCatIconFilePath = req.get('categoryIconPath')
	category = {
		"ResOwnerCatId": ResOwnerCatId,
		"ResCatVisibleIndex": ResCatVisibleIndex,
		"IsMain": IsMain,
		"ResCatName": ResCatName,
		"ResCatDesc": ResCatDesc,
		"ResCatIconName": ResCatIconName,
		"ResCatIconFilePath": ResCatIconFilePath
	}
	if(ResCatId != '' and ResCatId != None):
		category['ResCatId']=ResCatId
	category = configureNulls(category)
	return category

# category_fields = ['categoryOwner','categoryName','categoryDesc','categoryIcon']


def addRatingDict(req):
	RtId = req.get('ratingId')
	RtRemark = req.get('ratingRemark')
	RtRatingValue = req.get('ratingValue')
	RtValidated = req.get('ratingValidated')
	data = {
		"RtId": RtId,
		"RtRemark": RtRemark,
		"RtRatingValue": RtRatingValue,
		"RtValidated": RtValidated,
	}

	if(RtId != '' and RtId != None):
		data['RtId']=RtId
	data = configureNulls(data)
	return data


def addCompanyInfoDict(req):
	CName = req.get('companyName')
	CFullName = req.get('companyFullName')
	CDesc = req.get('companyDesc')
	AccInfId = req.get('companyAccInfId') # ??
	CAddress = req.get('companyAddress')
	CAddressLegal = req.get('companyAddressLegal')
	CLatitude = req.get('companyLatitude') 
	CLongitude = req.get('companyLongitude')  
	Phone1 = req.get('companyPhone1')
	Phone2 = req.get('companyPhone2')
	Phone3 = req.get('companyPhone3')
	Phone4 = req.get('companyPhone4')
	CPostalCode = req.get('companyPostalCode')
	CEmail = req.get('companyEmail')
	WebAddress = req.get('companyWebAddress')
	AddInf1 = req.get('companyWTime')
	companyInfo = {
		"CName": CName,
		"CFullName": CFullName,
		"CDesc": CDesc,
		"AccInfId": AccInfId,
		"CAddress": CAddress,
		"CAddressLegal": CAddressLegal,
		"CLatitude": CLatitude,
		"CLongitude": CLongitude,
		"Phone1": Phone1,
		"Phone2": Phone2,
		"Phone3": Phone3,
		"Phone4": Phone4,
		"CPostalCode": CPostalCode,
		"CEmail": CEmail,
		"WebAddress": WebAddress,
		"AddInf1": AddInf1
	}
	return companyInfo

# companyInfo_fields = ['companyName','companyFullName','companyDesc','companyAccInfId',
# 		'companyAddress','companyAddressLegal','companyLatitude','companyLongitude',
# 		'companyPhone1','companyPhone2','companyPhone3','companyPhone4',
# 		'companyPostalCode','companyEmail','companyWTime']


def addResourceDict(req):
	CId = req.get('companyId')
	DivId = req.get('divisionId')
	ResCatId = req.get('resCategoryId')
	UnitId = req.get('unitId')
	BrandId = req.get('brandId')
	UsageStatusId = req.get('usageStatusId')
	ResTypeId = req.get('resTypeId')
	ResMainImgId = req.get('mainImageId')
	ResMakerId = req.get('resMakerId')
	ResLastVendorId = req.get('lastVendorId')
	ResRegNo = req.get('resRegNo')
	ResName = req.get('resName')
	ResDesc = req.get('resDesc')
	ResFullDesc = req.get('resFullDesc')
	ResWidth = configureFloat(req.get('resWidth'))
	ResHeight = configureFloat(req.get('resHeight'))
	ResLength = configureFloat(req.get('resLength'))
	ResWeight = configureFloat(req.get('resWeight'))
	ResMinSaleAmount = configureFloat(req.get('resMinSaleAmount'))
	ResMaxSaleAmount = configureFloat(req.get('resMaxSaleAmount'))
	ResMinSalePrice = configureFloat(req.get('resMinSalePrice'))
	ResMaxSalePrice = configureFloat(req.get('resMaxSalePrice'))
	resource = {
		"CId": CId,
		"DivId": DivId,
		"ResCatId": ResCatId,
		"UnitId": UnitId,
		"BrandId": BrandId,
		"UsageStatusId": UsageStatusId,
		"ResTypeId": ResTypeId,
		"ResMainImgId": ResMainImgId,
		"ResMakerId": ResMakerId,
		"ResLastVendorId": ResLastVendorId,
		"ResRegNo": ResRegNo,
		"ResName": ResName,
		"ResDesc": ResDesc,
		"ResFullDesc": ResFullDesc,
		"ResWidth": ResWidth,
		"ResHeight": ResHeight,
		"ResLength": ResLength,
		"ResWeight": ResWeight,
		"ResMinSaleAmount": ResMinSaleAmount,
		"ResMaxSaleAmount": ResMaxSaleAmount,
		"ResMinSalePrice": ResMinSalePrice,
		"ResMaxSalePrice": ResMaxSalePrice
	}
	return resource

# resource_forms = ['resId','companyId','divisionId','resourceCategoryId','unitId',
# 	'brandId',	'usageStatusId','resourceTypeId','mainImageId','resourceMakerId',
# 	'lastVendorId','regNo','resourceName','resourceDesc','resourceFullDesc','resourceWidth',
# 	'resourceHeight','resourceLength','resourceWeight','resourceOnSale','resourceMinSaleAmount',
# 	'resourceMaxSaleAmount','resourceMinSalePrice','resourceMaxSalePrice']

def addBarcodeDict(req):
	CId = req.get('companyId')
	DivId = req.get('divisionId')
	ResId = req.get('resId')
	UnitId = req.get('unitId')
	BarcodeVal = req.get('barcodeVal')
	barcode = {
		"CId": CId,
		"DivId": DivId,
		"ResId": ResId,
		"UnitId": UnitId,
		"BarcodeVal": BarcodeVal
	}
	return barcode

# barcode_forms = ['barcodeId','companyId','divisionId','resId','unitId','barcodeVal']


def addBrandDict(req):
	BrandName = req.get('brandName')
	BrandDesc = req.get('brandDesc')
	brand = {
		"BrandName": BrandName,
		"BrandDesc": BrandDesc
	}
	return brand

# brand_forms = ['brandId','brandName','brandDesc']


def addColorDict(req):
	# ColorId = req.get('colorId')
	ColorName = req.get('colorName')
	ColorDesc = req.get('colorDesc')
	ColorCode = req.get('colorCode')
	color = {
		"ColorName": ColorName,
		"ColorDesc": ColorDesc,
		"ColorCode": ColorCode
	}
	return color

# color_forms = ['colorId','colorName','colorDesc','colorCode']

def addSizeDict(req):
	# SizeId = req.get('sizeId')
	SizeName = req.get('sizeName')
	SizeDesc = req.get('sizeDesc')
	SizeTypeId = req.get('sizeTypeId')
	size = {
		"SizeName": SizeName,
		"SizeDesc": SizeDesc,
		"SizeTypeId": SizeTypeId
	}
	return size

# size_forms = ['sizeId','sizeName','sizeDesc','sizeTypeId']

def addSizeTypeDict(req):
	# SizeTypeId = req.get('sizeTypeId')
	SizeTypeName = req.get('sizeTypeName')
	SizeTypeDesc = req.get('sizeTypeDesc')
	size_type = {
		"SizeTypeName": SizeTypeName,
		"SizeTypeDesc": SizeTypeDesc
	}
	return size_type

# size_type_forms = ['sizeTypeId','sizeTypeName','sizeTypeDesc']


def addResColorDict(req):
	# RcId = req.get('rcId')
	ResId = req.get('resId')
	ColorId = req.get('resColorId')
	res_color = {
		"ResId": ResId,
		"ColorId": ColorId
	}
	return res_color

# res_color_forms = ['rcId','resId','resColorId']

def addResSizeDict(req):
	# RsId = req.get('rsId')
	ResId = req.get('resId')
	SizeId = req.get('sizeId')
	res_size = {
		"ResId": ResId,
		"SizeId": SizeId
	}
	return res_size

# res_size_forms = ['rsId','resId','sizeId']

def addResPriceDict(req):
	# ResPriceId = req.get('resPriceId')
	ResPriceTypeId = req.get('resPriceTypeId')
	ResPriceGroupId = req.get('resPriceGroupId')
	UnitId = req.get('unitId')
	CurrencyId = req.get('currencyId')
	ResId = req.get('resId')
	ResPriceRegNo = req.get('resPriceRegNo')
	ResPriceValue = configureFloat(req.get('resPriceValue'))
	PriceStartDate = req.get('priceStartDate')
	PriceEndDate = req.get('priceEndDate')
	res_price = {
		# "ResPriceId": ResPriceId,
		"ResPriceTypeId": ResPriceTypeId,
		"ResPriceGroupId": ResPriceGroupId,
		"UnitId": UnitId,
		"CurrencyId": CurrencyId,
		"ResId": ResId,
		"ResPriceRegNo": ResPriceRegNo,
		"ResPriceValue": ResPriceValue,
		"PriceStartDate": PriceStartDate,
		"PriceEndDate": PriceEndDate
	}
	return res_price

# res_price_forms = ['resPriceId','resPriceTypeId','resPriceGroupId','unitId','currencyId',
# 	'resId','resPriceRegNo','resPriceValue','priceStartDate','priceEndDate']

def addResTransDict(req):
	# ResTansId = req.get('resTansId')
	ResId = req.get('resId')
	LangId = req.get('langId')
	ResName = req.get('resNameTrans')
	ResDesc = req.get('resDescTrans')
	ResFullDesc = req.get('resFullDescTrans')
	res_trans = {
		"ResId": ResId,
		"LangId": LangId,
		"ResName": ResName,
		"ResDesc": ResDesc,
		"ResFullDesc": ResFullDesc
	}
	return res_trans

# res_translations_forms = ['resTansId','resId','langId','resNameTrans','resDescTrans','resFullDescTrans']

def addLanguageDict(req):
	# LangId = req.get('langId')
	LangName = req.get('langName')
	LangDesc = req.get('langDesc')
	language = {
		"LangName": LangName,
		"LangDesc": LangDesc
	}
	return language

def addResUnitDict(req):
	# ResUnitId = req.get('resUnitId')
	ResId = req.get('resId')
	ResUnitUnitId = req.get('resUnitUnitId')
	ResUnitConvAmount = req.get('resUnitConvAmount')
	ResUnitConvTypeId = req.get('resUnitConvTypeId')
	res_unit = {
		"ResId": ResId,
		"ResUnitUnitId": ResUnitUnitId,
		"ResUnitConvAmount": ResUnitConvAmount,
		"ResUnitConvTypeId": ResUnitConvTypeId
	}
	return res_unit


def addImageDict(req):
	EmpId = req.get('empId')
	CId = req.get('companyId')
	RpAccId = req.get('rpAccId')
	ResId = req.get('resId')
	FileName = req.get('fileName')
	FileHash = req.get('fileHash')
	Image = req.get('image')
	image_dict = {
		"EmpId": EmpId,
		"CId": CId,
		"RpAccId": RpAccId,
		"ResId":ResId,
		"FileName":FileName,
		"FileHash":FileHash,
		"Image":Image,
		}
	return image_dict

# image_forms = ['imgId','empId''companyId''rpAccId''resId''fileName''fileHash''image']


############ useful methods ############# 
def configureFloat(value):
	try:
		value = float(value)
	except Exception as ex:
		value = 0
	return value

def boolCheck(value):
	if value == 'False' or value == 'false' or value == '0' or value == 0:
		value = False
	elif value: 
		value = True
	else:
		value = False
	return value

def dateDataCheck(date):
	try:
		date = datetime.strptime(date, "%Y-%m-%d")
	except Exception as ex:
		date = None
	return date

def configureNulls(data):
	for e in data:
		if data[e] == '':
			data[e] = None
	return data

def prepare_data(dropdown,page,title):
	template_data={
		"dropdown": dropdown,
		"page": page,
		"title": title,
	}
	return template_data