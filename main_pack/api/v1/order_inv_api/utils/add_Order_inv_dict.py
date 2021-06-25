# -*- coding: utf-8 -*-
import uuid
import dateutil.parser
from main_pack.base.dataMethods import configureNulls, configureFloat

def add_Order_inv_dict(req):
	OInvId = req.get('OInvId')
	OInvGuid = uuid.UUID(req.get('OInvGuid'))
	OInvTypeId = req.get('OInvTypeId')
	InvStatId = req.get('InvStatId')
	CurrencyId = req.get('CurrencyId')
	RpAccId = req.get('RpAccId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhId = req.get('WhId')
	WpId = req.get('WpId')
	EmpId = req.get('EmpId')
	PtId = req.get('PtId')
	PmId = req.get('PmId')
	PaymStatusId = req.get('PaymStatusId')
	OInvLatitude = configureFloat(req.get('OInvLatitude'))
	OInvLongitude = configureFloat(req.get('OInvLongitude'))
	OInvRegNo = req.get('OInvRegNo')
	OInvDesc = req.get('OInvDesc')
	OInvDate = dateutil.parser.parse(req.get('OInvDate')) if req.get('OInvDate') else None
	OInvTotal = configureFloat(req.get('OInvTotal'))
	OInvExpenseAmount = configureFloat(req.get('OInvExpenseAmount'))
	OInvTaxAmount = configureFloat(req.get('OInvTaxAmount'))
	OInvDiscountAmount = configureFloat(req.get('OInvDiscountAmount'))
	OInvFTotal = configureFloat(req.get('OInvFTotal'))
	OInvFTotalInWrite = req.get('OInvFTotalInWrite')
	OInvModifyCount = req.get('OInvModifyCount')
	OInvPrintCount = req.get('OInvPrintCount')
	OInvCreditDays = req.get('OInvCreditDays')
	OInvCreditDesc = req.get('OInvCreditDesc')
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
		"OInvGuid": OInvGuid,
		"OInvTypeId": OInvTypeId,
		"InvStatId": InvStatId,
		"CurrencyId": CurrencyId,
		"RpAccId": RpAccId,
		"CId": CId,
		"DivId": DivId,
		"WhId": WhId,
		"WpId": WpId,
		"EmpId": EmpId,
		"PtId": PtId,
		"PmId": PmId,
		"PaymStatusId": PaymStatusId,
		"OInvLatitude": OInvLatitude,
		"OInvLongitude": OInvLongitude,
		"OInvRegNo": OInvRegNo,
		"OInvDesc": OInvDesc,
		"OInvDate": OInvDate,
		"OInvTotal": OInvTotal,
		"OInvExpenseAmount": OInvExpenseAmount,
		"OInvTaxAmount": OInvTaxAmount,
		"OInvDiscountAmount": OInvDiscountAmount,
		"OInvFTotal": OInvFTotal,
		"OInvFTotalInWrite": OInvFTotalInWrite,
		"OInvModifyCount": OInvModifyCount,
		"OInvPrintCount": OInvPrintCount,
		"OInvCreditDays": OInvCreditDays,
		"OInvCreditDesc": OInvCreditDesc,
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

	#if(OInvId != '' and OInvId != None):
	#	data["OInvId"] = OInvId
	data = configureNulls(data)
	return data
