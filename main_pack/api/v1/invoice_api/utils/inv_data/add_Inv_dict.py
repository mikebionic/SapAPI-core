# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls, configureFloat

def add_Inv_dict(req):
	InvId = req.get('InvId')
	InvGuid = uuid.UUID(req.get('InvGuid'))
	InvTypeId = req.get('InvTypeId')
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
	InvLatitude = req.get('InvLatitude')
	InvLongitude = req.get('InvLongitude')
	InvRegNo = req.get('InvRegNo')
	InvDesc = req.get('InvDesc')
	InvDate = req.get('InvDate')
	InvTotal = configureFloat(req.get('InvTotal'))
	InvExpenseAmount = configureFloat(req.get('InvExpenseAmount'))
	InvTaxAmount = configureFloat(req.get('InvTaxAmount'))
	InvDiscountAmount = configureFloat(req.get('InvDiscountAmount'))
	InvFTotal = configureFloat(req.get('InvFTotal'))
	InvFTotalInWrite = req.get('InvFTotalInWrite')
	InvModifyCount = req.get('InvModifyCount')
	InvPrintCount = req.get('InvPrintCount')
	InvCreditDays = req.get('InvCreditDays')
	InvCreditDesc = req.get('InvCreditDesc')
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
		"InvTypeId": InvTypeId,
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
		"InvLatitude": InvLatitude,
		"InvLongitude": InvLongitude,
		"InvRegNo": InvRegNo,
		"InvDesc": InvDesc,
		"InvDate": InvDate,
		"InvTotal": InvTotal,
		"InvExpenseAmount": InvExpenseAmount,
		"InvTaxAmount": InvTaxAmount,
		"InvDiscountAmount": InvDiscountAmount,
		"InvFTotal": InvFTotal,
		"InvFTotalInWrite": InvFTotalInWrite,
		"InvModifyCount": InvModifyCount,	
		"InvPrintCount": InvPrintCount,
		"InvCreditDays": InvCreditDays,
		"InvCreditDesc": InvCreditDesc,
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
	#if(InvId != '' and InvId != None):
	#	data["InvId"] = InvId
	data = configureNulls(data)
	return data
