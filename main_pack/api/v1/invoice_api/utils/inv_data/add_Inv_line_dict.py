# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls, configureFloat


def add_Inv_line_dict(req):
	return configureNulls({
		#"InvLineId": req.get('InvLineId'),
		"InvLineGuid": req.get('InvLineGuid'),
		"InvId": req.get('InvId'),
		"UnitId": req.get('UnitId'),
		"CurrencyId": req.get('CurrencyId'),
		"ResId": req.get('ResId'),
		"LastVendorId": req.get('LastVendorId'),
		"InvLineRegNo": req.get('InvLineRegNo'),
		"InvLineDesc": req.get('InvLineDesc'),
		"InvLineAmount": req.get('InvLineAmount'),
		"InvLinePrice": req.get('InvLinePrice'),
		"InvLineTotal": req.get('InvLineTotal'),
		"InvLineExpenseAmount": req.get('InvLineExpenseAmount'),
		"InvLineTaxAmount": req.get('InvLineTaxAmount'),
		"InvLineDiscAmount": req.get('InvLineDiscAmount'),
		"InvLineFTotal": req.get('InvLineFTotal'),
		"InvLineDate": req.get('InvLineDate'),
		"ExcRateValue": req.get('ExcRateValue'),
		"AddInf1": req.get('AddInf1'),
		"AddInf2": req.get('AddInf2'),
		"AddInf3": req.get('AddInf3'),
		"AddInf4": req.get('AddInf4'),
		"AddInf5": req.get('AddInf5'),
		"AddInf6": req.get('AddInf6'),
		"CreatedDate": req.get('CreatedDate'),
		"ModifiedDate": req.get('ModifiedDate'),
		"SyncDateTime": req.get('SyncDateTime'),
		"CreatedUId": req.get('CreatedUId'),
		"ModifiedUId": req.get('ModifiedUId'),
		"GCRecord": req.get('GCRecord'),	
	})