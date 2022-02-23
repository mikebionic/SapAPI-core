# -*- coding: utf-8 -*-

from main_pack.models import Language

def collect_language_data(
	LangId = None,
	LangGuid = None,
	LangName = None,
	LangDesc = None,
):

	filtering = {"GCRecord": None}

	if LangId:
		filtering["LangId"] = LangId

	languages_query = Language.query.filter_by(**filtering)

	if LangName:
		languages_query = languages_query.filter(Language.LangName.ilike(f"%{LangName}%"))

	if LangDesc:
		languages_query = languages_query.filter(Language.LangDesc.ilike(f"%{LangDesc}%"))

	if LangGuid:
		languages_query = languages_query.filter(Language.LangGuid.ilike(f"%{LangGuid}%"))

	languages = languages_query.all()

	data = [lang.to_json_api() for lang in languages]

	return data