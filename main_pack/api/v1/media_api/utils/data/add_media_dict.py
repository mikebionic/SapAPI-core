# -*- coding: utf-8 -*-
import uuid
from main_pack.base.dataMethods import configureNulls

def add_media_dict(req):
	MediaId = req.get('MediaId')
	LangId = req.get('LangId')
	MediaCatId = req.get('MediaCatId')
	TagId = req.get('TagId')
	MediaGuid = uuid.UUID(req.get('MediaGuid')) if req.get('MediaGuid') else ''
	IsHidden = req.get('IsHidden')
	MediaName = req.get('MediaName')
	MediaTitle = req.get('MediaTitle')
	MediaDesc = req.get('MediaDesc')
	MediaBody = req.get('MediaBody')
	MediaAuthor = req.get('MediaAuthor')
	MediaUrl = req.get('MediaUrl')
	MediaDate = req.get('MediaDate')
	MediaIsFeatured = req.get('MediaIsFeatured')
	MediaViewCnt = req.get('MediaViewCnt')
	
	data = {
		# "MediaId": MediaId,
		"LangId": LangId,
		"MediaCatId": MediaCatId,
		"TagId": TagId,
		"MediaGuid": MediaGuid,
		"IsHidden": IsHidden,
		"MediaName": MediaName,
		"MediaTitle": MediaTitle,
		"MediaDesc": MediaDesc,
		"MediaBody": MediaBody,
		"MediaAuthor": MediaAuthor,
		"MediaUrl": MediaUrl,
		"MediaDate": MediaDate,
		"MediaIsFeatured": MediaIsFeatured,
		"MediaViewCnt": MediaViewCnt,
	}

	data = configureNulls(data)
	return data
