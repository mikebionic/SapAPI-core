# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_Translation_dict(req):
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

def add_Res_translation_dict(req):
	ResTranslGuid = uuid.UUID(req.get('ResTranslGuid')) if req.get('ResTranslGuid') else ""
	ResId = req.get('ResId')
	LangId = req.get('LangId')
	ResName = req.get('ResName')
	ResDesc = req.get('ResDesc')
	ResFullDesc = req.get('ResFullDesc')
	
	data = {
		"ResTranslGuid": ResTranslGuid,
		"ResId": ResId,
		"LangId": LangId,
		"ResName": ResName,
		"ResDesc": ResDesc,
		"ResFullDesc": ResFullDesc,
	}

	data = configureNulls(data)
	return data