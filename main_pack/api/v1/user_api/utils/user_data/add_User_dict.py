# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_User_dict(req):
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