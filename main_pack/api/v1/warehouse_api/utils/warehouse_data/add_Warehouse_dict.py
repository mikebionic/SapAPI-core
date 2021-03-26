# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_Warehouse_dict(req):
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
