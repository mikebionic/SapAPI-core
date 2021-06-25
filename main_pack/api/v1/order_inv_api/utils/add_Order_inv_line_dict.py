# -*- coding: utf-8 -*-
import uuid
import dateutil.parser

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
	OInvLineDate = dateutil.parser.parse(req.get('OInvLineDate')) if req.get('OInvLineDate') else None
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = dateutil.parser.parse(req.get('CreatedDate')) if req.get('CreatedDate') else None
	ModifiedDate = dateutil.parser.parse(req.get('ModifiedDate')) if req.get('ModifiedDate') else None
	SyncDateTime = dateutil.parser.parse(req.get('SyncDateTime')) if req.get('SyncDateTime') else None
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
