# -*- coding: utf-8 -*-
from flask import current_app
import uuid
import io
import os
import base64
from PIL import Image as ImageOperations
from main_pack import Config

from main_pack.base.imageMethods import save_image,dirHandler
from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck,configureEmptyQuotesNulls

def addCompanyDict(req):
	CId = req.get('CId')
	CName = req.get('CName')
	CFullName = req.get('CFullName')
	CDesc = req.get('CDesc')
	CGuid = uuid.UUID(req.get('CGuid'))
	AccInfId = req.get('AccInfId')
	CAddress = req.get('CAddress')
	CAddressLegal = req.get('CAddressLegal')
	CLatitude = req.get('CLatitude')
	CLongitude = req.get('CLongitude')
	Phone1 = req.get('Phone1')
	Phone2 = req.get('Phone2')
	Phone3 = req.get('Phone3')
	Phone4 = req.get('Phone4')
	CPostalCode = req.get('CPostalCode')
	WebAddress = req.get('WebAddress')
	CEmail = req.get('CEmail')
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

	company = {
		"CName": CName,
		"CFullName": CFullName,
		"CDesc": CDesc,
		"CGuid": CGuid,
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
		"WebAddress": WebAddress,
		"CEmail": CEmail,
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
	# if(CId != '' and CId != None):
	# 	company['CId'] = CId
	company = configureNulls(company)
	return company

def addDivisionDict(req):
	DivId = req.get('DivId')
	CId = req.get('CId')
	DivName = req.get('DivName')
	DivDesc = req.get('DivDesc')
	DivGuid = uuid.UUID(req.get('DivGuid'))
	OwnerDivisionId = req.get('OwnerDivisionId')
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

	division = {
		"CId": CId,
		"DivName": DivName,
		"DivDesc": DivDesc,
		"DivGuid": DivGuid,
		"OwnerDivisionId": OwnerDivisionId,
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
	# if(DivId != '' and DivId != None):
	# 	division['DivId'] = DivId
	division = configureNulls(division)
	return division

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
	# if(ResId != '' and ResId != None):
	# 	resource['ResId'] = ResId
	resource = configureNulls(resource)
	return resource

def addImageDict(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	ImgGuid = uuid.UUID(req.get('ImgGuid'))
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
		"ImgGuid": ImgGuid,
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
	# if(ImgId != '' and ImgId != None):
	# 	image['ImgId'] = ImgId
	image = configureNulls(image)
	return image

def saveImageFile(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	ImgGuid = uuid.UUID(req.get('ImgGuid'))
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
		"ImgGuid": ImgGuid,
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
	# if(ImgId != '' and ImgId != None):
	# 	image['ImgId'] = ImgId
	
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
		dumpImagePath = os.path.join(dumpFolderPath,f"dump.{Config.BLOB_TO_IMAGE_SAVE_EXT}")
		outfile = open(dumpImagePath,"wb")
		outfile.write(base64.decodebytes(imageBytes))
		outfile.flush()
		outfile.close()
		image_params = {
			"savedImage": dumpImagePath,
			"module": module,
			"id": id,
		}
		if image['ResId']:
			image_params["apply_watermark"] = True
		
		imageFile = save_image(**image_params)
		image['FilePath'] = imageFile['FilePath']
		image['FileName'] = imageFile['FileName']
		# for data in imageFile:
		# 	# Image db is currently not supporting this
		# 	# this will change later on
		# 	if data != "FilePath":
		# 		image[data]=imageFile[data]
	image = configureNulls(image)
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
	ResPriceValue = configureFloat(req.get('ResPriceValue'))
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
	# if(ResPriceId != '' and ResPriceId != None):
	# 	res_price['ResPriceId'] = ResPriceId
	res_price = configureNulls(res_price)
	return res_price

def addResTotalDict(req):
	ResTotId = req.get('ResTotId')
	ResId = req.get('ResId')
	CurrencyId = req.get('CurrencyId')
	WhId = req.get('WhId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WpId = req.get('WpId')
	ResTotBalance = configureFloat(req.get('ResTotBalance'))
	ResTotInAmount = configureFloat(req.get('ResTotInAmount'))
	ResTotOutAmount = configureFloat(req.get('ResTotOutAmount'))
	ResTotLastTrDate = req.get('ResTotLastTrDate')
	ResTotPurchAvgPrice = configureFloat(req.get('ResTotPurchAvgPrice'))
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

	# if(ResTotId != '' and ResTotId != None):
	# 	res_total['ResTotId'] = ResTotId
	res_total = configureEmptyQuotesNulls(res_total)
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
	rp_acc_trans_total = configureNulls(rp_acc_trans_total)
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
	PaymStatusId = req.get('PaymStatusId')
	OInvLatitude = configureFloat(req.get('OInvLatitude'))
	OInvLongitude = configureFloat(req.get('OInvLongitude'))
	OInvRegNo = req.get('OInvRegNo')
	OInvDesc = req.get('OInvDesc')
	OInvDate = req.get('OInvDate')
	OInvTotal = configureFloat(req.get('OInvTotal'))
	OInvExpenseAmount = configureFloat(req.get('OInvExpenseAmount'))
	OInvTaxAmount = configureFloat(req.get('OInvTaxAmount'))
	OInvDiscountAmount = configureFloat(req.get('OInvDiscountAmount'))
	OInvFTotal = configureFloat(req.get('OInvFTotal'))
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
		"PaymStatusId": PaymStatusId,
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
	order_inv = configureNulls(order_inv)
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
	OInvLineAmount = configureFloat(req.get('OInvLineAmount'))
	OInvLinePrice = configureFloat(req.get('OInvLinePrice'))
	OInvLineTotal = configureFloat(req.get('OInvLineTotal'))
	OInvLineExpenseAmount = configureFloat(req.get('OInvLineExpenseAmount'))
	OInvLineTaxAmount = configureFloat(req.get('OInvLineTaxAmount'))
	OInvLineDiscAmount = configureFloat(req.get('OInvLineDiscAmount'))
	OInvLineFTotal = configureFloat(req.get('OInvLineFTotal'))
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
	# if(OInvLineId != '' and OInvLineId != None):
	# 	order_inv_line['OInvLineId'] = OInvLineId
	order_inv_line = configureNulls(order_inv_line)
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
	order_inv_type = configureNulls(order_inv_type)
	return order_inv_type


def addInvDict(req):
	InvId = req.get('InvId')
	InvTypeId = req.get('InvTypeId')
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
	InvLatitude = req.get('InvLatitude')
	InvLongitude = req.get('InvLongitude')
	InvRegNo = req.get('InvRegNo')
	InvDesc = req.get('InvDesc')
	InvDate = req.get('InvDate')
	InvTotal = configureFloat(req.get('InvTotal'))
	InvExpenseAmount = configureFloat(req.get('InvExpenseAmount'))
	InvTaxAmount = configureFloat(req.get('InvTaxAmount'))
	InvDiscountAmount = configureFloat(req.get('InvDiscountAmount'))
	InvFTotal = configureFloat(req.get('InvFTotal'))
	InvFTotalInWrite = req.get('InvFTotalInWrite')
	InvModifyCount = req.get('InvModifyCount')
	InvPrintCount = req.get('InvPrintCount')
	InvCreditDays = req.get('InvCreditDays')
	InvCreditDesc = req.get('InvCreditDesc')
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
	inv = {
		"InvTypeId": InvTypeId,
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
		"InvLatitude": InvLatitude,
		"InvLongitude": InvLongitude,
		"InvRegNo": InvRegNo,
		"InvDesc": InvDesc,
		"InvDate": InvDate,
		"InvTotal": InvTotal,
		"InvExpenseAmount": InvExpenseAmount,
		"InvTaxAmount": InvTaxAmount,
		"InvDiscountAmount": InvDiscountAmount,
		"InvFTotal": InvFTotal,
		"InvFTotalInWrite": InvFTotalInWrite,
		"InvModifyCount": InvModifyCount,	
		"InvPrintCount": InvPrintCount,
		"InvCreditDays": InvCreditDays,
		"InvCreditDesc": InvCreditDesc,
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
	#if(InvId != '' and InvId != None):
	#	inv['InvId'] = InvId
	inv = configureNulls(inv)
	return inv


def addInvLineDict(req):
	InvLineId = req.get('InvLineId')
	InvId = req.get('InvId')
	UnitId = req.get('UnitId')
	CurrencyId = req.get('CurrencyId')
	ResId = req.get('ResId')
	LastVendorId = req.get('LastVendorId')
	InvLineDesc = req.get('InvLineDesc')
	InvLineAmount = req.get('InvLineAmount')
	InvLinePrice = configureFloat(req.get('InvLinePrice'))
	InvLineTotal = configureFloat(req.get('InvLineTotal'))
	InvLineExpenseAmount = configureFloat(req.get('InvLineExpenseAmount'))
	InvLineTaxAmount = configureFloat(req.get('InvLineTaxAmount'))
	InvLineDiscAmount = configureFloat(req.get('InvLineDiscAmount'))
	InvLineFTotal = configureFloat(req.get('InvLineFTotal'))
	InvLineDate = req.get('InvLineDate')
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

	inv_line = {
		"InvId": InvId,
		"UnitId": UnitId,
		"CurrencyId": CurrencyId,
		"ResId": ResId,
		"LastVendorId": LastVendorId,
		"InvLineDesc": InvLineDesc,
		"InvLineAmount": InvLineAmount,
		"InvLinePrice": InvLinePrice,
		"InvLineTotal": InvLineTotal,
		"InvLineExpenseAmount": InvLineExpenseAmount,
		"InvLineTaxAmount": InvLineTaxAmount,
		"InvLineDiscAmount": InvLineDiscAmount,
		"InvLineFTotal": InvLineFTotal,
		"InvLineDate": InvLineDate,
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
	# if(InvLineId != '' and InvLineId != None):
	# 	inv_line['InvLineId'] = InvLineId
	inv_line = configureNulls(inv_line)
	return inv_line


def addWarehouseDict(req):
	WhId = req.get('WhId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhName = req.get('WhName')
	WhDesc = req.get('WhDesc')
	UsageStatusId = req.get('UsageStatusId')
	WhGuid = uuid.UUID(req.get('WhGuid'))
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
		"WhGuid": WhGuid,
		"UsageStatusId": UsageStatusId,
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
	# if(WhId != '' and WhId != None):
	# 	warehouse['WhId'] = WhId
	warehouse = configureNulls(warehouse)
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
	work_period = configureNulls(work_period)
	return work_period