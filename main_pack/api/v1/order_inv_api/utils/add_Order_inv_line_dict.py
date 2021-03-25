# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls, configureFloat

def add_Order_inv_line_dict(req):
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
