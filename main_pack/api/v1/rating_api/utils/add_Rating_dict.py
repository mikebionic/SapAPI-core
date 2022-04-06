# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls


def add_Rating_dict(req):
	RtGuid = req.get('RtGuid')
	CId = req.get('CId')
	DivId = req.get('DivId')
	UId = req.get('UId')
	ResId = req.get('ResId')
	RpAccId = req.get('RpAccId')
	EmpId = req.get('EmpId')
	RtRemark = req.get('RtRemark')
	RtRatingValue = req.get('RtRatingValue')
	RtValidated = req.get('RtValidated')

	data = {
		"RtGuid": RtGuid,
		"CId": CId,
		"DivId": DivId,
		"UId": UId,
		"ResId": ResId,
		"RpAccId": RpAccId,
		"EmpId": EmpId,
		"RtRemark": RtRemark.strip() if RtRemark else '',
		"RtRatingValue": RtRatingValue,
		"RtValidated": RtValidated,
	}
	return configureNulls(data)

