# -*- coding: utf-8 -*-
# from main_pack.models.commerce.models import Res_category
from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck
from main_pack.base.imageMethods import save_image,dirHandler
import io
import os
import base64
from PIL import Image as ImageOperations
from flask import current_app

def addCategoryDict(req):
	ResCatId = req.get('ResCatId')
	ResOwnerCatId = req.get('ResOwnerCatId')
	ResCatName = req.get('ResCatName')
	ResCatDesc = req.get('ResCatDesc')
	ResCatIconName = req.get('ResCatIconName')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	category = {
		"ResOwnerCatId": ResOwnerCatId,
		"ResCatName": ResCatName,
		"ResCatDesc": ResCatDesc,
		"ResCatIconName": ResCatIconName,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	if(ResCatId != '' and ResCatId != None):
		category['ResCatId'] = ResCatId
	category=configureNulls(category)
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
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

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
		"ResProductionOnSale": ResProductionOnSale,
		"ResMinSaleAmount": ResMinSaleAmount,
		"ResMaxSaleAmount": ResMaxSaleAmount,
		"ResMinSalePrice": ResMinSalePrice,
		"ResMaxSalePrice": ResMaxSalePrice,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	if(ResId != '' and ResId != None):
		resource['ResId'] = ResId
	resource=configureNulls(resource)
	return resource

def addImageDict(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	FileName = req.get('FileName')
	FilePath = req.get('FilePath')
	FileHash = req.get('FileHash')
	# Image = str.encode(req.get('Image'))
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	image = {
		"EmpId": EmpId,
		"CId": CId,
		"RpAccId": RpAccId,
		"ResId": ResId,
		"FileName": FileName,
		"FilePath": FilePath,
		"FileHash": FileHash,
		# "Image": Image,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	if(ImgId != '' and ImgId != None):
		image['ImgId'] = ImgId
	image=configureNulls(image)
	return image

def saveImageFile(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	FileName = req.get('FileName')
	FilePath = req.get('FilePath')
	FileHash = req.get('FileHash')
	Image = str.encode(req.get('Image'))
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	image = {
		"EmpId": EmpId,
		"CId": CId,
		"RpAccId": RpAccId,
		"ResId": ResId,
		"FileName": FileName,
		"FilePath": FilePath,
		"FileHash": FileHash,
		# "Image": Image,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	if(ImgId != '' and ImgId != None):
		image['ImgId'] = ImgId
	# if blob presents:
	if Image:
		imageBytes = Image
		if image['RpAccId']:
			module = os.path.join("uploads","commmerce","Rp_acc")
			id = image['RpAccId']
		elif image['ResId']:
			module = os.path.join("uploads","commerce","Resource")
			id = image['ResId']
		elif image['EmpId']:
			module = os.path.join("uploads","Employee")
			id = image['EmpId']
		elif image['CId']:
			module = os.path.join("uploads","Company")
			id = image['CId']
		elif image['UId']:
			module = os.path.join("uploads","Users")
			id = image['UId']
		else:
			module = None
			id = None

		dumpFolderPath = os.path.join(current_app.root_path,'static','imageDumps')
		dirHandler(dumpFolderPath)
		dumpImagePath = os.path.join(dumpFolderPath,"dump.jpg")
		outfile = open(dumpImagePath,"wb")
		outfile.write(base64.decodebytes(imageBytes))
		outfile.flush()
		outfile.close()
		imageFile = save_image(savedImage=dumpImagePath,module=module,id=id)
		image['FilePath'] = imageFile['FilePath']
		image['FileName'] = imageFile['FileName']
		# for data in imageFile:
		# 	# Image db is currently not supporting this
		# 	# this will change later on
		# 	if data != "FilePath":
		# 		image[data]=imageFile[data]
	image=configureNulls(image)
	return image

def addBarcodeDict(req):
	BarcodeId = req.get('BarcodeId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	ResId = req.get('ResId')
	UnitId = req.get('UnitId')
	BarcodeVal = req.get('BarcodeVal')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	barcode = {
		"CId": CId,
		"DivId": DivId,
		"ResId": ResId,
		"UnitId": UnitId,
		"BarcodeVal": BarcodeVal,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(BarcodeId != '' and BarcodeId != None):
		barcode['BarcodeId'] = BarcodeId
	barcode = configureNulls(barcode)
	return	barcode

def addResPriceDict(req):
	ResPriceId = req.get('ResPriceId')
	ResPriceTypeId = req.get('ResPriceTypeId')
	ResPriceGroupId = req.get('ResPriceGroupId')
	UnitId = req.get('UnitId')
	CurrencyId = req.get('CurrencyId')
	ResId = req.get('ResId')
	ResPriceRegNo = req.get('ResPriceRegNo')
	ResPriceValue = req.get('ResPriceValue')
	PriceStartDate = req.get('PriceStartDate')
	PriceEndDate = req.get('PriceEndDate')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	res_price = {
		"ResPriceTypeId": ResPriceTypeId,
		"ResPriceGroupId": ResPriceGroupId,
		"UnitId": UnitId,
		"CurrencyId": CurrencyId,
		"ResId": ResId,
		"ResPriceRegNo": ResPriceRegNo,
		"ResPriceValue": ResPriceValue,
		"PriceStartDate": PriceStartDate,
		"PriceEndDate": PriceEndDate,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(ResPriceId != '' and ResPriceId != None):
		res_price['ResPriceId'] = ResPriceId
	res_price=configureNulls(res_price)
	return res_price

def addResTotalDict(req):
	ResTotId = req.get('ResTotId')
	ResId = req.get('ResId')
	CurrencyId = req.get('CurrencyId')
	WhId = req.get('WhId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WpId = req.get('WpId')
	ResTotBalance = req.get('ResTotBalance')
	ResTotInAmount = req.get('ResTotInAmount')
	ResTotOutAmount = req.get('ResTotOutAmount')
	ResTotLastTrDate = req.get('ResTotLastTrDate')
	ResTotPurchAvgPrice = req.get('ResTotPurchAvgPrice')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	res_total = {
		"ResId": ResId,
		"CurrencyId": CurrencyId,
		"WhId": WhId,
		"CId": CId,
		"DivId": DivId,
		"WpId": WpId,
		"ResTotBalance": ResTotBalance,
		"ResTotInAmount": ResTotInAmount,
		"ResTotOutAmount": ResTotOutAmount,
		"ResTotLastTrDate": ResTotLastTrDate,
		"ResTotPurchAvgPrice": ResTotPurchAvgPrice,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	if(ResTotId != '' and ResTotId != None):
		res_total['ResTotId'] = ResTotId
	res_total=configureNulls(res_total)
	return res_total


def addRpAccTrTotDict(req):
	RpAccTrTotId = req.get('RpAccTrTotId')
	RpAccId = req.get('RpAccId')
	CurrencyId = req.get('CurrencyId')
	RpAccTrTotBalance = req.get('RpAccTrTotBalance')
	RpAccTrTotDebit = req.get('RpAccTrTotDebit')
	RpAccTrTotCredit = req.get('RpAccTrTotCredit')
	RpAccTrTotLastTrDate = req.get('RpAccTrTotLastTrDate')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	rp_acc_trans_total={
		"RpAccId": RpAccId,
		"CurrencyId": CurrencyId,
		"RpAccTrTotBalance": RpAccTrTotBalance,
		"RpAccTrTotDebit": RpAccTrTotDebit,
		"RpAccTrTotCredit": RpAccTrTotCredit,
		"RpAccTrTotLastTrDate": RpAccTrTotLastTrDate,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	if(RpAccTrTotId != '' and RpAccTrTotId != None):
		rp_acc_trans_total['RpAccTrTotId'] = RpAccTrTotId
	rp_acc_trans_total=configureNulls(rp_acc_trans_total)
	return rp_acc_trans_total


def addOrderInvDict(req):
	OInvId = req.get('OInvId')
	OInvTypeId = req.get('OInvTypeId')
	InvStatId = req.get('InvStatId')
	CurrencyId = req.get('CurrencyId')
	RpAccId = req.get('RpAccId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhId = req.get('WhId')
	WpId = req.get('WpId')
	EmpId = req.get('EmpId')
	PtId = req.get('PtId')
	PmId = req.get('PmId')
	OInvLatitude = req.get('OInvLatitude')
	OInvLongitude = req.get('OInvLongitude')
	OInvRegNo = req.get('OInvRegNo')
	OInvDesc = req.get('OInvDesc')
	OInvDate = req.get('OInvDate')
	OInvTotal = req.get('OInvTotal')
	OInvExpenseAmount = req.get('OInvExpenseAmount')
	OInvTaxAmount = req.get('OInvTaxAmount')
	OInvDiscountAmount = req.get('OInvDiscountAmount')
	OInvFTotal = req.get('OInvFTotal')
	OInvFTotalInWrite = req.get('OInvFTotalInWrite')
	OInvModifyCount = req.get('OInvModifyCount')
	OInvPrintCount = req.get('OInvPrintCount')
	OInvCreditDays = req.get('OInvCreditDays')
	OInvCreditDesc = req.get('OInvCreditDesc')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	order_inv = {
		"OInvTypeId": OInvTypeId,
		"InvStatId": InvStatId,
		"CurrencyId": CurrencyId,
		"RpAccId": RpAccId,
		"CId": CId,
		"DivId": DivId,
		"WhId": WhId,
		"WpId": WpId,
		"EmpId": EmpId,
		"PtId": PtId,
		"PmId": PmId,
		"OInvLatitude": OInvLatitude,
		"OInvLongitude": OInvLongitude,
		"OInvRegNo": OInvRegNo,
		"OInvDesc": OInvDesc,
		"OInvDate": OInvDate,
		"OInvTotal": OInvTotal,
		"OInvExpenseAmount": OInvExpenseAmount,
		"OInvTaxAmount": OInvTaxAmount,
		"OInvDiscountAmount": OInvDiscountAmount,
		"OInvFTotal": OInvFTotal,
		"OInvFTotalInWrite": OInvFTotalInWrite,
		"OInvModifyCount": OInvModifyCount,
		"OInvPrintCount": OInvPrintCount,
		"OInvCreditDays": OInvCreditDays,
		"OInvCreditDesc": OInvCreditDesc,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	#if(OInvId != '' and OInvId != None):
	#	order_inv['OInvId'] = OInvId
	order_inv=configureNulls(order_inv)
	return order_inv

def addOrderInvLineDict(req):
	OInvLineId = req.get('OInvLineId')
	OInvId = req.get('OInvId')
	UnitId = req.get('UnitId')
	CurrencyId = req.get('CurrencyId')
	ResId = req.get('ResId')
	LastVendorId = req.get('LastVendorId')
	OInvLineRegNo = req.get('OInvLineRegNo')
	OInvLineDesc = req.get('OInvLineDesc')
	OInvLineAmount = req.get('OInvLineAmount')
	OInvLinePrice = req.get('OInvLinePrice')
	OInvLineTotal = req.get('OInvLineTotal')
	OInvLineExpenseAmount = req.get('OInvLineExpenseAmount')
	OInvLineTaxAmount = req.get('OInvLineTaxAmount')
	OInvLineDiscAmount = req.get('OInvLineDiscAmount')
	OInvLineFTotal = req.get('OInvLineFTotal')
	OInvLineDate = req.get('OInvLineDate')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	order_inv_line = {
		#"OInvId": OInvId,
		"UnitId": UnitId,
		"CurrencyId": CurrencyId,
		"ResId": ResId,
		"LastVendorId": LastVendorId,
		"OInvLineRegNo": OInvLineRegNo,
		"OInvLineDesc": OInvLineDesc,
		"OInvLineAmount": OInvLineAmount,
		"OInvLinePrice": OInvLinePrice,
		"OInvLineTotal": OInvLineTotal,
		"OInvLineExpenseAmount": OInvLineExpenseAmount,
		"OInvLineTaxAmount": OInvLineTaxAmount,
		"OInvLineDiscAmount": OInvLineDiscAmount,
		"OInvLineFTotal": OInvLineFTotal,
		"OInvLineDate": OInvLineDate,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(OInvLineId != '' and OInvLineId != None):
		order_inv_line['OInvLineId'] = OInvLineId
	order_inv_line=configureNulls(order_inv_line)
	return order_inv_line

def addOrderInvTypeDict(req):
	OInvTypeId = req.get('OInvTypeId')
	OInvTypeName_tkTM = req.get('OInvTypeName_tkTM')
	OInvTypeDesc_tkTM = req.get('OInvTypeDesc_tkTM')
	OInvTypeName_ruRU = req.get('OInvTypeName_ruRU')
	OInvTypeDesc_ruRU = req.get('OInvTypeDesc_ruRU')
	OInvTypeName_enUS = req.get('OInvTypeName_enUS')
	OInvTypeDesc_enUS = req.get('OInvTypeDesc_enUS')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	order_inv_type = {
		"OInvTypeName_tkTM": OInvTypeName_tkTM,
		"OInvTypeDesc_tkTM": OInvTypeDesc_tkTM,
		"OInvTypeName_ruRU": OInvTypeName_ruRU,
		"OInvTypeDesc_ruRU": OInvTypeDesc_ruRU,
		"OInvTypeName_enUS": OInvTypeName_enUS,
		"OInvTypeDesc_enUS": OInvTypeDesc_enUS,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(OInvTypeId != '' and OInvTypeId != None):
		order_inv_type['OInvTypeId'] = OInvTypeId
	order_inv_type=configureNulls(order_inv_type)
	return order_inv_type

def addWarehouseDict(req):
	WhId = req.get('WhId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhName = req.get('WhName')
	WhDesc = req.get('WhDesc')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	warehouse = {
		"CId": CId,
		"DivId": DivId,
		"WhName": WhName,
		"WhDesc": WhDesc,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(WhId != '' and WhId != None):
		warehouse['WhId'] = WhId
	warehouse=configureNulls(warehouse)
	return warehouse

def addWorkPeriodDict(req):
	WpId = req.get('WpId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	CurrencyId = req.get('CurrencyId')
	WpStartDate = req.get('WpStartDate')
	WpEndDate = req.get('WpEndDate')
	WpIsDefault = req.get('WpIsDefault')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	work_period = {
		"CId": CId,
		"DivId": DivId,
		"CurrencyId": CurrencyId,
		"WpStartDate": WpStartDate,
		"WpEndDate": WpEndDate,
		"WpIsDefault": WpIsDefault,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	if(WpId != '' and WpId != None):
		work_period['WpId'] = WpId
	work_period=configureNulls(work_period)
	return work_period