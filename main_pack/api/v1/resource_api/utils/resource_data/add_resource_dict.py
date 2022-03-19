# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_resource_dict(req):
	ResId = req.get('ResId')
	ResGuid = uuid.UUID(req.get('ResGuid'))
	ResUniqueId = req.get('ResUniqueId')
	UId = req.get('UId')
	RpAccId = req.get('RpAccId')
	ResName = req.get('ResName')
	ResDesc = req.get('ResDesc')
	AllowedDate = req.get('AllowedDate')
	DisallowedDate = req.get('DisallowedDate')
	IsAllowed = req.get('IsAllowed')
	ResVerifyDate = req.get('ResVerifyDate')
	ResVerifyKey = req.get('ResVerifyKey')
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
		"ResGuid": ResGuid,
		"ResUniqueId": ResUniqueId,
		"UId": UId,
		"RpAccId": RpAccId,
		"ResName": ResName,
		"ResDesc": ResDesc,
		"AllowedDate": AllowedDate,
		"DisallowedDate": DisallowedDate,
		"IsAllowed": IsAllowed,
		"ResVerifyDate": ResVerifyDate,
		"ResVerifyKey": ResVerifyKey,
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
	# 	users["ResId"] = ResId
	users = configureNulls(users)
	return users