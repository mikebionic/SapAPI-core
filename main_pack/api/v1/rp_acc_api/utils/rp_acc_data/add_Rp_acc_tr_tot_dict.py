# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls


def add_Rp_acc_tr_tot_dict(req):
	RpAccTrTotId = req.get('RpAccTrTotId')
	RpAccId = req.get('RpAccId')
	CurrencyId = req.get('CurrencyId')
	RpAccTrTotBalance = req.get('RpAccTrTotBalance')
	RpAccTrTotDebit = req.get('RpAccTrTotDebit')
	RpAccTrTotCredit = req.get('RpAccTrTotCredit')
	RpAccTrTotLastTrDate = req.get('RpAccTrTotLastTrDate')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	SyncDateTime = req.get('SyncDateTime')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	data = {
		"RpAccId": RpAccId,
		"CurrencyId": CurrencyId,
		"RpAccTrTotBalance": RpAccTrTotBalance,
		"RpAccTrTotDebit": RpAccTrTotDebit,
		"RpAccTrTotCredit": RpAccTrTotCredit,
		"RpAccTrTotLastTrDate": RpAccTrTotLastTrDate,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"SyncDateTime": SyncDateTime,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}

	# if(RpAccTrTotId != '' and RpAccTrTotId != None):
	# 	data["RpAccTrTotId"] = RpAccTrTotId
	data = configureNulls(data)
	return data

