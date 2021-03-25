# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_Rp_acc_dict(req):
	RpAccId = req.get('RpAccId')
	RpAccGuid = uuid.UUID(req.get('RpAccGuid'))
	UId = req.get('UId')
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
	RpAccUName = req.get('RpAccUName')
	RpAccUPass = req.get('RpAccUPass')
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
	RpAccLatitude = req.get('RpAccLatitude')
	RpAccLongitude = req.get('RpAccLongitude')
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
		"RpAccGuid": RpAccGuid,
		"UId": UId,
		"CId": CId,
		"DivId": DivId,
		"EmpId": EmpId,
		"GenderId": GenderId,
		"NatId": NatId,
		"RpAccStatusId": RpAccStatusId,
		"ReprId": ReprId,
		"RpAccTypeId": RpAccTypeId,
		"WpId": WpId,
		"RpAccRegNo": RpAccRegNo,
		"RpAccName": RpAccName,
		"RpAccUName": RpAccUName,
		"RpAccUPass": RpAccUPass,
		"RpAccAddress": RpAccAddress,
		"RpAccMobilePhoneNumber": RpAccMobilePhoneNumber,
		"RpAccHomePhoneNumber": RpAccHomePhoneNumber,
		"RpAccWorkPhoneNumber": RpAccWorkPhoneNumber,
		"RpAccWorkFaxNumber": RpAccWorkFaxNumber,
		"RpAccZipCode": RpAccZipCode,
		"RpAccEMail": RpAccEMail,
		"RpAccFirstName": RpAccFirstName,
		"RpAccLastName": RpAccLastName,
		"RpAccPatronomic": RpAccPatronomic,
		"RpAccBirthDate": RpAccBirthDate,
		"RpAccResidency": RpAccResidency,
		"RpAccPassportNo": RpAccPassportNo,
		"RpAccPassportIssuePlace": RpAccPassportIssuePlace,
		"RpAccLangSkills": RpAccLangSkills,
		"RpAccSaleBalanceLimit": RpAccSaleBalanceLimit,
		"RpAccPurchBalanceLimit": RpAccPurchBalanceLimit,
		"RpAccLatitude": RpAccLatitude,
		"RpAccLongitude": RpAccLongitude,
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
	# if(RpAccId != '' and RpAccId != None):
	# 	print(RpAccId)
	# 	data["RpAccId"] = RpAccId
	data = configureNulls(data)
	return data