def addCategoryDict(req):
	ResOwnerCatId = req.get('ownerCategory')
	ResCatName = req.get('categoryName')
	ResCatDesc = req.get('categoryDesc')
	ResCatIconName = req.get('categoryIcon')
	category = {
		'ResOwnerCatId':ResOwnerCatId,
		'ResCatName':ResCatName,
		'ResCatDesc':ResCatDesc,
		'ResCatIconName':ResCatIconName
	}
	category = configureNulls(category)
	return category

# category_fields = ['ownerCategory','categoryName','categoryDesc','categoryIcon']

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
	CWTime = req.get('companyWTime')
	companyInfo = {
		'CName':CName,
		'CFullName':CFullName,
		'CDesc':CDesc,
		'AccInfId':AccInfId,
		'CAddress':CAddress,
		'CAddressLegal':CAddressLegal,
		'CLatitude':CLatitude,
		'CLongitude':CLongitude,
		'Phone1':Phone1,
		'Phone2':Phone2,
		'Phone3':Phone3,
		'Phone4':Phone4,
		'CPostalCode':CPostalCode,
		'CEmail':CEmail,
		'CWTime':CWTime
	}
	return companyInfo

# companyInfo_fields = ['companyName','companyFullName','companyDesc','companyAccInfId',
# 		'companyAddress','companyAddressLegal','companyLatitude','companyLongitude',
# 		'companyPhone1','companyPhone2','companyPhone3','companyPhone4',
# 		'companyPostalCode','companyEmail','companyWTime']


def addResourceDict(req):
	CId = req.get('companyId')
	DivId = req.get('divisionId')
	ResCatId = req.get('resourceCategoryId')
	UnitId = req.get('unitId')
	BrandId = req.get('brandId')
	UsageStatusId = req.get('usageStatusId')
	ResourceTypeId = req.get('resourceTypeId')
	ResMainImgId = req.get('mainImageId')
	ResMakerId = req.get('resourceMakerId')
	ResLastVendorId = req.get('lastVendorId')
	ResRegNo = req.get('regNo')
	ResName = req.get('resourceName')
	ResDesc = req.get('resourceDesc')
	ResFullDesc = req.get('resourceFullDesc')
	ResWidth = req.get('resourceWidth')
	ResHeight = req.get('resourceHeight')
	ResLength = req.get('resourceLength')
	ResWeight = req.get('resourceWeight')
	ResProductionOnSale = req.get('resourceOnSale')
	ResMinSaleAmount = req.get('resourceMinSaleAmount')
	ResMaxSaleAmount = req.get('resourceMaxSaleAmount')
	ResMinSalePrice = req.get('resourceMinSalePrice')
	ResMaxSalePrice = req.get('resourceMaxSalePrice')
	resource = {
		'CId':CId,
		'DivId':DivId,
		'ResCatId':ResCatId,
		'UnitId':UnitId,
		'BrandId':BrandId,
		'UsageStatusId':UsageStatusId,
		'ResourceTypeId':ResourceTypeId,
		'ResMainImgId':ResMainImgId,
		'ResMakerId':ResMakerId,
		'ResLastVendorId':ResLastVendorId,
		'ResRegNo':ResRegNo,
		'ResName':ResName,
		'ResDesc':ResDesc,
		'ResFullDesc':ResFullDesc,
		'ResWidth':ResWidth,
		'ResHeight':ResHeight,
		'ResLength':ResLength,
		'ResWeight':ResWeight,
		'ResProductionOnSale':ResProductionOnSale,
		'ResMinSaleAmount':ResMinSaleAmount,
		'ResMaxSaleAmount':ResMaxSaleAmount,
		'ResMinSalePrice':ResMinSalePrice,
		'ResMaxSalePrice':ResMaxSalePrice
	}
	return resource

# resource_forms = ['resourceId','companyId','divisionId','resourceCategoryId','unitId',
# 	'brandId',	'usageStatusId','resourceTypeId','mainImageId','resourceMakerId',
# 	'lastVendorId','regNo','resourceName','resourceDesc','resourceFullDesc','resourceWidth',
# 	'resourceHeight','resourceLength','resourceWeight','resourceOnSale','resourceMinSaleAmount',
# 	'resourceMaxSaleAmount','resourceMinSalePrice','resourceMaxSalePrice']

def addBarcodeDict(req):
	CId = req.get('companyId')
	DivId = req.get('divisionId')
	ResId = req.get('resourceId')
	UnitId = req.get('unitId')
	BarcodeVal = req.get('barcodeVal')
	barcode = {
		'companyId':CId,
		'divisionId':DivId,
		'resourceId':ResId,
		'unitId':UnitId,
		'barcodeVal':BarcodeVal
	}
	return barcode

# barcode_forms = ['companyId','divisionId','resourceId','unitId','barcodeVal']


def addBrandDict(req):
	BrandName = req.get('brandName')
	BrandDesc = req.get('brandDesc')
	brand = {
		'brandName':BrandName,
		'brandDesc':BrandDesc
	}
	return brand

# brand_forms = ['brandId','brandDesc']






############ useful methods ############# 
def boolCheck(value):
	if value == 'False' or value == 'false' or value == '0' or value == 0:
		value = False
	elif value: 
		value = True
	else:
		value = False
	return value
	print(value)

def dateDataCheck(date):
	try:
		date = datetime.strptime(date, "%Y-%m-%d")
	except:
		date = None
	return date

def configureNulls(data):
	for e in data:
		if data[e] == '':
			data[e] = None
	return data

def prepare_data(dropdown,page,title):
	template_data={
		'dropdown': dropdown,
		'page': page,
		'title': title,
	}
	return template_data