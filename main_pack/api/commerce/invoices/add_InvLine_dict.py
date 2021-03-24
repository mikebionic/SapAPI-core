# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls, configureFloat

def add_InvLine_dict(req):
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
