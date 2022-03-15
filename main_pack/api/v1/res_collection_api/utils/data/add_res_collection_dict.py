# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_res_collection_dict(req):
	ResCollectionGuid = uuid.UUID(req.get('ResCollectionGuid')) if req.get('ResCollectionGuid') else ""
	# CId = req.get('CId')
	# DivId = req.get('DivId')
	ResCollectionName = req.get('ResCollectionName')
	ResCollectionDesc = req.get('ResCollectionDesc')
	ResCollectionPrice = req.get('ResCollectionPrice')

	data = {
		"ResCollectionGuid": ResCollectionGuid,
		# "CId": CId,
		# "DivId": DivId,
		"ResCollectionName": ResCollectionName,
		"ResCollectionDesc": ResCollectionDesc,
		"ResCollectionPrice": ResCollectionPrice,
	}

	data = configureNulls(data)
	return data

def add_res_collection_line_dict(req):
	ResCollectionLineGuid = uuid.UUID(req.get('ResCollectionLineGuid')) if req.get('ResCollectionLineGuid') else ""
	# ResCollectionId = req.get('ResCollectionId')
	UnitId = req.get('UnitId')
	# ResId = req.get('ResId')
	ResCollectionLineAmount = req.get('ResCollectionLineAmount')
	ResCollectionLinePrice = req.get('ResCollectionLinePrice')
	ResCollectionLineDesc = req.get('ResCollectionLineDesc')

	data = {
		"ResCollectionLineGuid": ResCollectionLineGuid,
		# "ResCollectionId": ResCollectionId,
		"UnitId": UnitId,
		# "ResId": ResId,
		"ResCollectionLineAmount": ResCollectionLineAmount,
		"ResCollectionLinePrice": ResCollectionLinePrice,
		"ResCollectionLineDesc": ResCollectionLineDesc,
	}

	data = configureNulls(data)
	return data