# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_Device_dict(req):
	DevId = req.get('DevId')
	DevGuid = uuid.UUID(req.get('DevGuid'))
	DevUniqueId = req.get('DevUniqueId')
	UId = req.get('UId')
	RpAccId = req.get('RpAccId')
	DevName = req.get('DevName')
	DevDesc = req.get('DevDesc')
	AllowedDate = req.get('AllowedDate')
	DisallowedDate = req.get('DisallowedDate')
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

	users = {
		"DevGuid": DevGuid,
		"DevUniqueId": DevUniqueId,
		"UId": UId,
		"RpAccId": RpAccId,
		"DevName": DevName,
		"DevDesc": DevDesc,
		"AllowedDate": AllowedDate,
		"DisallowedDate": DisallowedDate,
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
	# if(DevId != '' and DevId != None):
	# 	users["DevId"] = DevId
	users = configureNulls(users)
	return users