# -*- coding: utf-8 -*-
import uuid
from sqlalchemy.orm import joinedload

from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.apiMethods import fileToURL
from main_pack.base.dataMethods import configureNulls, configureFloat, boolCheck


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
	DbGuid = uuid.UUID('DbGuid')
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
		"DbGuid": DbGuid,
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

def addDeviceDict(req):
	DevId = req.get('DevId')
	DevGuid = req.get('DevGuid')
	DevUniqueId = req.get('DevUniqueId')
	RpAccId = req.get('RpAccId')
	DevName = req.get('DevName')
	DevDesc = req.get('DevDesc')
	IsAllowed = req.get('IsAllowed')
	DevVerifyDate = req.get('DevVerifyDate')
	DevVerifyKey = req.get('DevVerifyKey')
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

	json_data = {
		# "DevId": DevId,
		"DevGuid": DevGuid,
		"DevUniqueId": DevUniqueId,
		"RpAccId": RpAccId,
		"DevName": DevName,
		"DevDesc": DevDesc,
		"IsAllowed": IsAllowed,
		"DevVerifyDate": DevVerifyDate,
		"DevVerifyKey": DevVerifyKey,
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

	# RpAccId shouldn't merge, but should be relatively taken
	json_data["RpAccId"] = None
	return json_data
	

###### returning info for single user after api auth success #####
from main_pack.models import Image
from main_pack.models import Resource
from main_pack.base.apiMethods import fileToURL
from main_pack.models import User, Rp_acc, User_type
from sqlalchemy import and_


def apiUsersData(
	UId = None,
	dbQuery = None,
	dbModel = None,
	rpAccInfo = True,
	additionalInfo = True):

	if not dbModel:

		if not dbQuery:
			dbQuery = User.query.filter_by(GCRecord = None, UId = UId)

		dbQuery = dbQuery.options(joinedload(User.Image))

		if rpAccInfo:
			dbQuery = dbQuery.options(joinedload(User.Rp_acc))

		if additionalInfo:
			dbQuery = dbQuery.options(joinedload(User.user_type))

		dbModel = dbQuery.first()

	data = {}
	if dbModel:
		data = dbModel.to_json_api()

		List_Images = [image.to_json_api() for image in dbModel.Image if not image.GCRecord]
		List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))

		data["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["Images"] = List_Images if List_Images else []

		if rpAccInfo:
			data["Rp_accs"] = [rp_acc.to_json_api() for rp_acc in dbModel.Rp_acc if not rp_acc.GCRecord]

		if additionalInfo:
			data["User_type"] = dataLangSelector(dbModel.user_type.to_json_api()) if dbModel.user_type else {}

	res = {
		"status": 1 if len(data) > 0 else 0,
		"data": data,
		"total": len(data)
	}
	return res


def apiRpAccData(
	RpAccRegNo = None,
	dbQuery = None,
	dbModel = None,
	userInfo = True,
	additionalInfo = True):

	if not dbModel:

		if not dbQuery:
			dbQuery = Rp_acc.query.filter_by(GCRecord = None, RpAccRegNo = RpAccRegNo)

		dbQuery = dbQuery.options(joinedload(Rp_acc.Image))

		if userInfo:
			dbQuery = dbQuery.options(joinedload(Rp_acc.user))

		if additionalInfo:
			dbQuery = dbQuery.options(
				joinedload(Rp_acc.rp_acc_type),
				joinedload(Rp_acc.rp_acc_status))

		dbModel = dbQuery.first()

	data = {}
	if dbModel:
		data = dbModel.to_json_api()

		List_Images = [image.to_json_api() for image in dbModel.Image if not image.GCRecord]
		List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))

		data["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		data["Images"] = List_Images if List_Images else []


		if userInfo:
			data["User"] = dbModel.user.to_json_api() if dbModel.user and not dbModel.user.GCRecord else {}
	
		if additionalInfo:
			data["Rp_acc_type"] = dataLangSelector(dbModel.rp_acc_type.to_json_api()) if dbModel.rp_acc_type else {}
			data["Rp_acc_status"] = dataLangSelector(dbModel.rp_acc_status.to_json_api()) if dbModel.rp_acc_status else {}

	res = {
		"status": 1 if len(data) > 0 else 0,
		"data": data,
		"total": len(data)
	}
	return res


def apiDeviceData(dbQuery=None, dbModel=None):
	if not dbModel:
		dbModel = dbQuery.first()

	data = {}

	if dbModel:
		data = dbModel.to_json_api()

	res = {
		"status": 1 if len(data) > 0 else 0,
		"data": data,
		"total": len(data)
	}
	return res