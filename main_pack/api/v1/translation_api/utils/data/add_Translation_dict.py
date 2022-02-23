# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_Translation_dict(req):
	TranslId = req.get('TranslId')
	TranslGuid = uuid.UUID(req.get('TranslGuid')) if req.get('TranslGuid') else ""
	ResCatId = req.get('ResCatId')
	ColorId = req.get('ColorId')
	ProdId = req.get('ProdId')
	SlImgId = req.get('SlImgId')
	LangId = req.get('LangId')
	TranslName = req.get('TranslName')
	TranslDesc = req.get('TranslDesc')
	
	data = {
		# "TranslId": TranslId,
		"TranslGuid": TranslGuid,
		"ResCatId": ResCatId,
		"ColorId": ColorId,
		"ProdId": ProdId,
		"SlImgId": SlImgId,
		"LangId": LangId,
		"TranslName": TranslName,
		"TranslDesc": TranslDesc
	}

	data = configureNulls(data)
	return data
