# -*- coding: utf-8 -*-
from sqlalchemy.orm import joinedload

from main_pack.models import Res_translation, Language, Resource

def collect_res_translation_data(
	ResTranslId = None,
	ResTranslGuid = None,
	ResId = None,
	ResName = None,
	ResGuid = None,
	ResTranslName = None,
	ResTranslDesc = None,
	LangName = None,
	LangId = None,
	showResource = 0,
):
	data = []

	filtering = {"GCRecord": None}

	if ResTranslId:
		filtering["ResTranslId"] = ResTranslId

	if ResTranslGuid:
		filtering["ResTranslGuid"] = ResTranslGuid

	if LangId:
		filtering["LangId"] = LangId

	if LangName:
		this_language = Language.query.filter(Language.LangName.ilike(f"%{LangName}%")).first()
		if this_language:
			filtering["LangId"] = this_language.LangId

	if ResId:
		filtering["ResId"] = ResId
	if ResGuid:
		this_resource = Resource.query.filter(Resource.ResGuid == ResGuid).first()
		if this_resource:
			filtering["ResId"] = this_resource.ResId
	elif ResName:
			this_resource = Resource.query.filter(Resource.ResName.ilike(f"%{ResName}%")).first()
			if this_resource:
				filtering["ResId"] = this_resource.ResId

	db_translations = Res_translation.query.filter_by(**filtering)

	if ResTranslName:
		db_translations = db_translations.filter(Res_translation.ResTranslName.ilike(f"%{ResTranslName}%"))

	if ResTranslDesc:
		db_translations = db_translations.filter(Res_translation.ResTranslDesc.ilike(f"%{ResTranslDesc}%"))


	db_translations = db_translations.options(joinedload(Res_translation.language))
	if showResource:
		db_translations = db_translations.options(joinedload(Res_translation.resource))

	db_translations = db_translations.order_by(Res_translation.ResTranslId.desc())\
	.all()

	for translation_data in db_translations:
		this_data = translation_data.to_json_api()
		this_data["LangName"] = translation_data.language.LangName if translation_data.language else ""
		if showResource:
			this_data["Resource"] = translation_data.resource.to_json_api() if translation_data.resource else {}
		data.append(this_data)
	return data