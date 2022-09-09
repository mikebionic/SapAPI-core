# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_res_request_dict(req):
	ResReqGuid = uuid.UUID(req.get('ResReqGuid')) if req.get('ResReqGuid') else ""
	# CId = req.get('CId')
	# DivId = req.get('DivId')
	ResReqName = req.get('ResReqName')
	ResReqDesc = req.get('ResReqDesc')
	ResReqImageUrl = req.get('ResReqImageUrl') if req.get('ResReqImageUrl') else ""
	ClientName = req.get('ClientName')
	ClientEmail = req.get('ClientEmail')
	ClientPhoneNumber = req.get('ClientPhoneNumber')

	data = {
		"ResReqGuid": ResReqGuid,
		# "CId": CId,
		# "DivId": DivId,
		"ResReqName": ResReqName,
		"ResReqDesc": ResReqDesc,
		"ResReqImageUrl": ResReqImageUrl,
		"ClientName": ClientName,
		"ClientEmail": ClientEmail,
		"ClientPhoneNumber": ClientPhoneNumber,
	}

	data = configureNulls(data)
	return data