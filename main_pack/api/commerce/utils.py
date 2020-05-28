# from main_pack.models.commerce.models import Res_category
from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck

def addCategoryDict(req):
	ResCatId = req.get('ResCatId')
	ResOwnerCatId = req.get('ResOwnerCatId')
	ResCatName = req.get('ResCatName')
	ResCatDesc = req.get('ResCatDesc')
	ResCatIconName = req.get('ResCatIconName')
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

	category = {
		'ResCatId':ResCatId,
		'ResOwnerCatId':ResOwnerCatId,
		'ResCatName':ResCatName,
		'ResCatDesc':ResCatDesc,
		'ResCatIconName':ResCatIconName,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
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
		'ResMaxSalePrice':ResMaxSalePrice,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
	}
	if(ResId != '' and ResId != None):
		print(ResId)
		resource['ResId']=ResId
	resource=configureNulls(resource)
	return resource

def addImageDict(req):
	ImgId = req.get('ImgId')
	EmpId = req.get('EmpId')
	CId = req.get('CId')
	RpAccId = req.get('RpAccId')
	ResId = req.get('ResId')
	FileName = req.get('FileName')
	FileHash = req.get('FileHash')
	Image = req.get('Image')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	image = {
		'EmpId':EmpId,
		'CId':CId,
		'RpAccId':RpAccId,
		'ResId':ResId,
		'FileName':FileName,
		'FileHash':FileHash,
		'Image':Image,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
	}
	if(ImgId != '' and ImgId != None):
		print(ImgId)
		image['ImgId']=ImgId
	image=configureNulls(image)
	return image

def addRpAccDict(req):
	RpAccId = req.get('RpAccId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	EmpId = req.get('EmpId')
	GenderId = req.get('GenderId')
	NatId = req.get('NatId')
	RpAccStatusId = req.get('RpAccStatusId')
	ReprId = req.get('ReprId')
	RpAccTypeId = req.get('RpAccTypeId')
	WpId = req.get('WpId')
	RpAccRegNo = req.get('RpAccRegNo')
	RpAccName = req.get('RpAccName')
	RpAccAddress = req.get('RpAccAddress')
	RpAccMobilePhoneNumber = req.get('RpAccMobilePhoneNumber')
	RpAccHomePhoneNumber = req.get('RpAccHomePhoneNumber')
	RpAccWorkPhoneNumber = req.get('RpAccWorkPhoneNumber')
	RpAccWorkFaxNumber = req.get('RpAccWorkFaxNumber')
	RpAccZipCode = req.get('RpAccZipCode')
	RpAccEMail = req.get('RpAccEMail')
	RpAccFirstName = req.get('RpAccFirstName')
	RpAccLastName = req.get('RpAccLastName')
	RpAccPatronomic = req.get('RpAccPatronomic')
	RpAccBirthDate = req.get('RpAccBirthDate')
	RpAccResidency = req.get('RpAccResidency')
	RpAccPassportNo = req.get('RpAccPassportNo')
	RpAccPassportIssuePlace = req.get('RpAccPassportIssuePlace')
	RpAccLangSkills = req.get('RpAccLangSkills')
	RpAccSaleBalanceLimit = req.get('RpAccSaleBalanceLimit')
	RpAccPurchBalanceLimit = req.get('RpAccPurchBalanceLimit')
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
	rp_acc = {		
		'CId':CId,
		'DivId':DivId,
		'EmpId':EmpId,
		'GenderId':GenderId,
		'NatId':NatId,
		'RpAccStatusId':RpAccStatusId,
		'ReprId':ReprId,
		'RpAccTypeId':RpAccTypeId,
		'WpId':WpId,
		'RpAccRegNo':RpAccRegNo,
		'RpAccName':RpAccName,
		'RpAccAddress':RpAccAddress,
		'RpAccMobilePhoneNumber':RpAccMobilePhoneNumber,
		'RpAccHomePhoneNumber':RpAccHomePhoneNumber,
		'RpAccWorkPhoneNumber':RpAccWorkPhoneNumber,
		'RpAccWorkFaxNumber':RpAccWorkFaxNumber,
		'RpAccZipCode':RpAccZipCode,
		'RpAccEMail':RpAccEMail,
		'RpAccFirstName':RpAccFirstName,
		'RpAccLastName':RpAccLastName,
		'RpAccPatronomic':RpAccPatronomic,
		'RpAccBirthDate':RpAccBirthDate,
		'RpAccResidency':RpAccResidency,
		'RpAccPassportNo':RpAccPassportNo,
		'RpAccPassportIssuePlace':RpAccPassportIssuePlace,
		'RpAccLangSkills':RpAccLangSkills,
		'RpAccSaleBalanceLimit':RpAccSaleBalanceLimit,
		'RpAccPurchBalanceLimit':RpAccPurchBalanceLimit,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
		}
	if(RpAccId != '' and RpAccId != None):
		print(RpAccId)
		rp_acc['RpAccId']=RpAccId
	rp_acc = configureNulls(rp_acc)
	return rp_acc


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
		'CId':self.CId,
		'DivId':self.DivId,
		'ResId':self.ResId,
		'UnitId':self.UnitId,
		'BarcodeVal':self.BarcodeVal,
		'CreatedDate':self.CreatedDate,
		'ModifiedDate':self.ModifiedDate,
		'CreatedUId':self.CreatedUId,
		'ModifiedUId':self.ModifiedUId,
		'GCRecord':self.GCRecord
		}
	if(BarcodeId != '' and BarcodeId != None):
		barcode['BarcodeId']=BarcodeId
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
		'ResPriceTypeId':ResPriceTypeId,
		'ResPriceGroupId':ResPriceGroupId,
		'UnitId':UnitId,
		'CurrencyId':CurrencyId,
		'ResId':ResId,
		'ResPriceRegNo':ResPriceRegNo,
		'ResPriceValue':ResPriceValue,
		'PriceStartDate':PriceStartDate,
		'PriceEndDate':PriceEndDate,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
		}
	if(ResPriceId != '' and ResPriceId != None):
		print(ResPriceId)
		res_price['ResPriceId']=ResPriceId
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
		'ResId':self.ResId,
		'CurrencyId':self.CurrencyId,
		'WhId':self.WhId,
		'CId':self.CId,
		'DivId':self.DivId,
		'WpId':self.WpId,
		'ResTotBalance':self.ResTotBalance,
		'ResTotInAmount':self.ResTotInAmount,
		'ResTotOutAmount':self.ResTotOutAmount,
		'ResTotLastTrDate':self.ResTotLastTrDate,
		'ResTotPurchAvgPrice':self.ResTotPurchAvgPrice,
		'CreatedDate':self.CreatedDate,
		'ModifiedDate':self.ModifiedDate,
		'CreatedUId':self.CreatedUId,
		'ModifiedUId':self.ModifiedUId,
		'GCRecord':self.GCRecord
	}
	
	if(ResTotId != '' and ResTotId != None):
		res_total['ResTotId']=ResTotId
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
		'RpAccId':self.RpAccId,
		'CurrencyId':self.CurrencyId,
		'RpAccTrTotBalance':self.RpAccTrTotBalance,
		'RpAccTrTotDebit':self.RpAccTrTotDebit,
		'RpAccTrTotCredit':self.RpAccTrTotCredit,
		'RpAccTrTotLastTrDate':self.RpAccTrTotLastTrDate,
		'CreatedDate':self.CreatedDate,
		'ModifiedDate':self.ModifiedDate,
		'CreatedUId':self.CreatedUId,
		'ModifiedUId':self.ModifiedUId,
		'GCRecord':self.GCRecord
	}
	
	if(RpAccTrTotId != '' and RpAccTrTotId != None):
		rp_acc_trans_total['RpAccTrTotId']=RpAccTrTotId
	rp_acc_trans_total=configureNulls(rp_acc_trans_total)
	return rp_acc_trans_total
