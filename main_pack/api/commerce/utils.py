from main_pack.models.commerce.models import Res_category
from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck

def addCategoryDict(req):
	ResCatId = req.get('ResCatId')
	ResOwnerCatId = req.get('ResOwnerCatId')
	ResCatName = req.get('ResCatName')
	ResCatDesc = req.get('ResCatDesc')
	ResCatIconName = req.get('ResCatIconName')
	category = {
		'ResCatId':ResCatId,
		'ResOwnerCatId':ResOwnerCatId,
		'ResCatName':ResCatName,
		'ResCatDesc':ResCatDesc,
		'ResCatIconName':ResCatIconName
	}
	category = configureNulls(category)
	return category

def addResourceDict(req):
	ResId = req.get('ResId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	ResCatId = req.get('ResCatId')
	UnitId = req.get('UnitId')
	BrandId = req.get('BrandId')
	UsageStatusId = req.get('UsageStatusId')
	ResTypeId = req.get('ResTypeId')
	ResMainImgId = req.get('ResMainImgId')
	ResMakerId = req.get('ResMakerId')
	ResLastVendorId = req.get('ResLastVendorId')
	ResRegNo = req.get('ResRegNo')
	ResName = req.get('ResName')
	ResDesc = req.get('ResDesc')
	ResFullDesc = req.get('ResFullDesc')
	ResWidth = configureFloat(req.get('ResWidth'))
	ResHeight = configureFloat(req.get('ResHeight'))
	ResLength = configureFloat(req.get('ResLength'))
	ResWeight = configureFloat(req.get('ResWeight'))
	ResProductionOnSale = boolCheck(req.get('ResProductionOnSale'))
	ResMinSaleAmount = configureFloat(req.get('ResMinSaleAmount'))
	ResMaxSaleAmount = configureFloat(req.get('ResMaxSaleAmount'))
	ResMinSalePrice = configureFloat(req.get('ResMinSalePrice'))
	ResMaxSalePrice = configureFloat(req.get('ResMaxSalePrice'))
	resource = {
		'ResId':ResId,
		'CId':CId,
		'DivId':DivId,
		'ResCatId':ResCatId,
		'UnitId':UnitId,
		'BrandId':BrandId,
		'UsageStatusId':UsageStatusId,
		'ResTypeId':ResTypeId,
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
	resource=configureNulls(resource)
	return resource