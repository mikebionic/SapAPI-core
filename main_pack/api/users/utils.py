# -*- coding: utf-8 -*-
import uuid
from sqlalchemy.orm import joinedload

from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.apiMethods import fileToURL
from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck


def addUsersDict(req):
	UId = req.get('UId')
	UGuid = uuid.UUID(req.get('UGuid'))
	CId = req.get('CId')
	DivId = req.get('DivId')
	RpAccId = req.get('RpAccId')
	UFullName = req.get('UFullName')
	UName = req.get('UName')
	UEmail = req.get('UEmail')
	UPass = req.get('UPass')
	URegNo = req.get('URegNo')
	UShortName = req.get('UShortName')
	EmpId = req.get('EmpId')
	UTypeId = req.get('UTypeId')
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

	users = {
		"UGuid": UGuid,
		"CId": CId,
		"DivId": DivId,
		"RpAccId": RpAccId,
		"UFullName": UFullName,
		"UName": UName,
		"UEmail": UEmail,
		"UPass": UPass,
		"URegNo": URegNo,
		"UShortName": UShortName,
		"EmpId": EmpId,
		"UTypeId": UTypeId,
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
	# if(UId != '' and UId != None):
	# 	users["UId"] = UId
	users = configureNulls(users)
	return users

def addRpAccDict(req):
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
	rp_acc = {
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
	# 	rp_acc["RpAccId"] = RpAccId
	rp_acc = configureNulls(rp_acc)
	return rp_acc


###### returning info for single user after api auth success #####
from main_pack.models.base.models import Image
from main_pack.models.commerce.models import Resource
from main_pack.base.apiMethods import fileToURL
from main_pack.models.users.models import Users,Rp_acc,User_type
from sqlalchemy import and_

def apiUsersData(UId=None, dbQuery=None):
	if not dbQuery:
		dbQuery = Users.query.filter_by(GCRecord = None, UId = UId)

	dbQuery = dbQuery.options(
		joinedload(Users.Image),
		joinedload(Users.Rp_acc),
		joinedload(Users.user_type))\
	.first()

	data = {}
	if dbQuery:
		data = dbQuery.to_json_api()

		List_Images = [image.to_json_api() for image in dbQuery.Image if image.GCRecord == None]
		List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))

		data["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["Images"] = List_Images if List_Images else []
		data["Rp_accs"] = [rp_acc.to_json_api() for rp_acc in dbQuery.Rp_acc if rp_acc.GCRecord == None]
		data["User_type"] = dataLangSelector(dbQuery.user_type.to_json_api()) if dbQuery.user_type else {}

	res = {
		"status":1,
		"data":data,
		"total":1
	}
	return res


def apiRpAccData(RpAccRegNo=None, dbQuery=None, dbModel=None):
	if not dbModel:
		if not dbQuery:
			dbQuery = Rp_acc.query.filter_by(GCRecord = None, RpAccRegNo = RpAccRegNo)

		dbModel = dbQuery.options(
			joinedload(Rp_acc.Image),
			joinedload(Rp_acc.users),
			joinedload(Rp_acc.rp_acc_type),
			joinedload(Rp_acc.rp_acc_status))\
		.first()

	data = {}
	if dbModel:
		data = dbModel.to_json_api()

		List_Images = [image.to_json_api() for image in dbModel.Image if image.GCRecord == None]
		List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))

		data["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["Images"] = List_Images if List_Images else []


		data["User"] = dbModel.users.to_json_api() if dbModel.users and dbModel.users.GCRecord == None else {}
		data["Rp_acc_type"] = dataLangSelector(dbModel.rp_acc_type.to_json_api()) if dbModel.rp_acc_type else {}
		data["Rp_acc_status"] = dataLangSelector(dbModel.rp_acc_status.to_json_api()) if dbModel.rp_acc_status else {}

	res = {
		"status": 1,
		"data": data,
		"total": 1
	}
	return res