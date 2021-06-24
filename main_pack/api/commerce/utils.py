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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(CId != '' and CId != None):
	# 	data["CId"] = CId
	data = configureNulls(data)
	return data

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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(DivId != '' and DivId != None):
	# 	data["DivId"] = DivId
	data = configureNulls(data)
	return data

def addCategoryDict(req):
	ResCatId = req.get('ResCatId')
	ResCatGuid = uuid.UUID(req.get('ResCatGuid')) if req.get('ResCatGuid') else None
	ResOwnerCatId = req.get('ResOwnerCatId')
	ResCatVisibleIndex = req.get('ResCatVisibleIndex')
	IsMain = req.get('IsMain')
	ResCatName = req.get('ResCatName')
	ResCatDesc = req.get('ResCatDesc')
	ResCatIconName = req.get('ResCatIconName')
	ResCatIconFilePath = req.get('ResCatIconFilePath')
	ResCatIconData = req.get('ResCatIconData')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"ResCatGuid": ResCatGuid,
		"ResOwnerCatId": ResOwnerCatId,
		"ResCatVisibleIndex": ResCatVisibleIndex,
		"IsMain": IsMain,
		"ResCatName": ResCatName,
		"ResCatDesc": ResCatDesc,
		"ResCatIconName": ResCatIconName,
		"ResCatIconFilePath": ResCatIconFilePath,
		"ResCatIconData": ResCatIconData,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord,
	}

	if(ResCatId != '' and ResCatId != None):
		data["ResCatId"] = ResCatId
	data = configureNulls(data)
	return data

def addResourceDict(req):
	ResId = req.get('ResId')
	ResGuid = uuid.UUID(req.get('ResGuid'))
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"ResGuid": ResGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(ResId != '' and ResId != None):
	# 	data["ResId"] = ResId
	data = configureNulls(data)
	return data

def addImageDict(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	UId = req.get('UId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	ImgGuid = uuid.UUID(req.get('ImgGuid'))
	FileName = req.get('FileName')
	FilePath = req.get('FilePath')
	FileHash = req.get('FileHash')
	MinDarkFileName = req.get('MinDarkFileName')
	MinDarkFilePath = req.get('MinDarkFilePath')
	MaxDarkFileName = req.get('MaxDarkFileName')
	MaxDarkFilePath = req.get('MaxDarkFilePath')
	MinLightFileName = req.get('MinLightFileName')
	MinLightFilePath = req.get('MinLightFilePath')
	MaxLightFileName = req.get('MaxLightFileName')
	MaxLightFilePath = req.get('MaxLightFilePath')
	# Image = str.encode(req.get('Image'))
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"EmpId": EmpId,
		"CId": CId,
		"UId": UId,
		"RpAccId": RpAccId,
		"ResId": ResId,
		"ImgGuid": ImgGuid,
		"FileName": FileName,
		"FilePath": FilePath,
		"FileHash": FileHash,
		"MinDarkFileName": MinDarkFileName,
		"MinDarkFilePath": MinDarkFilePath,
		"MaxDarkFileName": MaxDarkFileName,
		"MaxDarkFilePath": MaxDarkFilePath,
		"MinLightFileName": MinLightFileName,
		"MinLightFilePath": MinLightFilePath,
		"MaxLightFileName": MaxLightFileName,
		"MaxLightFilePath": MaxLightFilePath,
		# "Image": Image,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(ImgId != '' and ImgId != None):
	# 	data["ImgId"] = ImgId
	data = configureNulls(data)
	return data

def saveImageFile(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	UId = req.get('UId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	ImgGuid = uuid.UUID(req.get('ImgGuid'))
	FileName = req.get('FileName')
	FilePath = req.get('FilePath')
	FileHash = req.get('FileHash')
	MinDarkFileName = req.get('MinDarkFileName')
	MinDarkFilePath = req.get('MinDarkFilePath')
	MaxDarkFileName = req.get('MaxDarkFileName')
	MaxDarkFilePath = req.get('MaxDarkFilePath')
	MinLightFileName = req.get('MinLightFileName')
	MinLightFilePath = req.get('MinLightFilePath')
	MaxLightFileName = req.get('MaxLightFileName')
	MaxLightFilePath = req.get('MaxLightFilePath')	
	Image = str.encode(req.get('Image'))
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	image = {
		"EmpId": EmpId,
		"CId": CId,
		"UId": UId,
		"RpAccId": RpAccId,
		"ResId": ResId,
		"ImgGuid": ImgGuid,
		"FileName": FileName,
		"FilePath": FilePath,
		"FileHash": FileHash,
		"MinDarkFileName": MinDarkFileName,
		"MinDarkFilePath": MinDarkFilePath,
		"MaxDarkFileName": MaxDarkFileName,
		"MaxDarkFilePath": MaxDarkFilePath,
		"MinLightFileName": MinLightFileName,
		"MinLightFilePath": MinLightFilePath,
		"MaxLightFileName": MaxLightFileName,
		"MaxLightFilePath": MaxLightFilePath,
		# "Image": Image,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	# if(ImgId != '' and ImgId != None):
	# 	image["ImgId"] = ImgId
	
	# if blob presents:
	if Image:
		imageBytes = Image
		if image["RpAccId"]:
			module = os.path.join("uploads","commmerce","Rp_acc")
			id = image["RpAccId"]
		elif image["ResId"]:
			module = os.path.join("uploads","commerce","Resource")
			id = image["ResId"]
		elif image["EmpId"]:
			module = os.path.join("uploads","Employee")
			id = image["EmpId"]
		elif image["CId"]:
			module = os.path.join("uploads","Company")
			id = image["CId"]
		elif image["UId"]:
			module = os.path.join("uploads","User")
			id = image["UId"]
		else:
			module = None
			id = None

		dumpFolderPath = os.path.join(Config.STATIC_FOLDER_LOCATION, 'imageDumps')
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
		if image["ResId"]:
			image_params["apply_watermark"] = True
		
		if (image["FileName"] and Config.USE_PROVIDED_IMAGE_FILENAME == True):
			image_params["image_name"] = image["FileName"]
		imageFile = save_image(**image_params)
		image["FilePath"] = imageFile["FilePath"]
		image["FileName"] = imageFile["FileName"]
		# for data in imageFile:
		# 	# Image db is currently not supporting this
		# 	# this will change later on
		# 	if data != "FilePath":
		# 		image[data]=imageFile[data]
	image = configureNulls(image)
	return image

def addBarcodeDict(req):
	BarcodeId = req.get('BarcodeId')
	BarcodeGuid = uuid.UUID(req.get('BarcodeGuid')) if req.get('BarcodeGuid') else None
	CId = req.get('CId')
	DivId = req.get('DivId')
	ResId = req.get('ResId')
	UnitId = req.get('UnitId')
	BarcodeVal = req.get('BarcodeVal')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"BarcodeGuid": BarcodeGuid,
		"CId": CId,
		"DivId": DivId,
		"ResId": ResId,
		"UnitId": UnitId,
		"BarcodeVal": BarcodeVal,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	# if(BarcodeId != '' and BarcodeId != None):
	# 	data["BarcodeId"] = BarcodeId
	data = configureNulls(data)
	return	data

def addResPriceDict(req):
	ResPriceId = req.get('ResPriceId')
	ResPriceGuid = uuid.UUID(req.get('ResPriceGuid')) if req.get('ResPriceGuid') else None
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"ResPriceGuid": ResPriceGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	# if(ResPriceId != '' and ResPriceId != None):
	# 	data["ResPriceId"] = ResPriceId
	data = configureNulls(data)
	return data

def addResTotalDict(req):
	ResTotId = req.get('ResTotId')
	ResTotGuid = uuid.UUID(req.get('ResTotGuid')) if req.get('ResTotGuid') else None
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"ResTotGuid": ResTotGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(ResTotId != '' and ResTotId != None):
	# 	data["ResTotId"] = ResTotId
	data = configureEmptyQuotesNulls(data)
	return data


def addRpAccTrTotDict(req):
	RpAccTrTotId = req.get('RpAccTrTotId')
	RpAccTrTotGuid = uuid.UUID(req.get('RpAccTrTotGuid')) if req.get('RpAccTrTotGuid') else None
	RpAccId = req.get('RpAccId')
	CurrencyId = req.get('CurrencyId')
	RpAccTrTotBalance = req.get('RpAccTrTotBalance')
	RpAccTrTotDebit = req.get('RpAccTrTotDebit')
	RpAccTrTotCredit = req.get('RpAccTrTotCredit')
	RpAccTrTotLastTrDate = req.get('RpAccTrTotLastTrDate')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"RpAccTrTotGuid": RpAccTrTotGuid,
		"RpAccId": RpAccId,
		"CurrencyId": CurrencyId,
		"RpAccTrTotBalance": RpAccTrTotBalance,
		"RpAccTrTotDebit": RpAccTrTotDebit,
		"RpAccTrTotCredit": RpAccTrTotCredit,
		"RpAccTrTotLastTrDate": RpAccTrTotLastTrDate,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	if(RpAccTrTotId != '' and RpAccTrTotId != None):
		data["RpAccTrTotId"] = RpAccTrTotId
	data = configureNulls(data)
	return data


def addOrderInvDict(req):
	OInvId = req.get('OInvId')
	OInvGuid = uuid.UUID(req.get('OInvGuid'))
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"OInvGuid": OInvGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	#if(OInvId != '' and OInvId != None):
	#	data["OInvId"] = OInvId
	data = configureNulls(data)
	return data


def addOrderInvLineDict(req):
	OInvLineId = req.get('OInvLineId')
	OInvId = req.get('OInvId')
	OInvLineGuid = uuid.UUID(req.get('OInvLineGuid'))
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		#"OInvId": OInvId,
		"OInvLineGuid": OInvLineGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	# if(OInvLineId != '' and OInvLineId != None):
	# 	data["OInvLineId"] = OInvLineId
	data = configureNulls(data)
	return data

def addOrderInvTypeDict(req):
	OInvTypeId = req.get('OInvTypeId')
	OInvTypeGuid = uuid.UUID(req.get('OInvTypeGuid')) if req.get('OInvTypeGuid') else None
	OInvTypeName_tkTM = req.get('OInvTypeName_tkTM')
	OInvTypeDesc_tkTM = req.get('OInvTypeDesc_tkTM')
	OInvTypeName_ruRU = req.get('OInvTypeName_ruRU')
	OInvTypeDesc_ruRU = req.get('OInvTypeDesc_ruRU')
	OInvTypeName_enUS = req.get('OInvTypeName_enUS')
	OInvTypeDesc_enUS = req.get('OInvTypeDesc_enUS')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"OInvTypeGuid": OInvTypeGuid,
		"OInvTypeName_tkTM": OInvTypeName_tkTM,
		"OInvTypeDesc_tkTM": OInvTypeDesc_tkTM,
		"OInvTypeName_ruRU": OInvTypeName_ruRU,
		"OInvTypeDesc_ruRU": OInvTypeDesc_ruRU,
		"OInvTypeName_enUS": OInvTypeName_enUS,
		"OInvTypeDesc_enUS": OInvTypeDesc_enUS,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	if(OInvTypeId != '' and OInvTypeId != None):
		data["OInvTypeId"] = OInvTypeId
	data = configureNulls(data)
	return data


def addInvDict(req):
	InvId = req.get('InvId')
	InvGuid = uuid.UUID(req.get('InvGuid'))
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')	

	data = {
		"InvGuid": InvGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}
	#if(InvId != '' and InvId != None):
	#	data["InvId"] = InvId
	data = configureNulls(data)
	return data


def addInvLineDict(req):
	InvLineId = req.get('InvLineId')
	InvGuid = uuid.UUID(req.get('InvGuid'))
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
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"InvGuid": InvGuid,
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	# if(InvLineId != '' and InvLineId != None):
	# 	data["InvLineId"] = InvLineId
	data = configureNulls(data)
	return data


def addWarehouseDict(req):
	WhId = req.get('WhId')
	WhGuid = uuid.UUID(req.get('WhGuid'))
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhName = req.get('WhName')
	WhDesc = req.get('WhDesc')
	UsageStatusId = req.get('UsageStatusId')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
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
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	# if(WhId != '' and WhId != None):
	# 	data["WhId"] = WhId
	data = configureNulls(data)
	return data

def addWorkPeriodDict(req):
	WpId = req.get('WpId')
	WpGuid = uuid.UUID(req.get('WpGuid')) if req.get('WpGuid') else None
	CId = req.get('CId')
	DivId = req.get('DivId')
	CurrencyId = req.get('CurrencyId')
	WpStartDate = req.get('WpStartDate')
	WpEndDate = req.get('WpEndDate')
	WpIsDefault = req.get('WpIsDefault')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"WpGuid": WpGuid,
		"CId": CId,
		"DivId": DivId,
		"CurrencyId": CurrencyId,
		"WpStartDate": WpStartDate,
		"WpEndDate": WpEndDate,
		"WpIsDefault": WpIsDefault,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	if(WpId != '' and WpId != None):
		data["WpId"] = WpId
	data = configureNulls(data)
	return data


def addExcRateDict(req):
	ExcRateId = req.get('ExcRateId')
	ExcRateGuid = req.get(req.get('ExcRateGuid')) if req.get('ExcRateGuid') else None
	CurrencyId = req.get('CurrencyId')
	ExcRateDate = req.get('ExcRateDate')
	ExcRateInValue = req.get('ExcRateInValue')
	ExcRateOutValue = req.get('ExcRateOutValue')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		# "ExcRateId": ExcRateId,
		"ExcRateGuid": ExcRateGuid,
		"CurrencyId": CurrencyId,
		"ExcRateDate": ExcRateDate,
		"ExcRateInValue": ExcRateInValue,
		"ExcRateOutValue": ExcRateOutValue,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
		}

	data = configureNulls(data)
	return data