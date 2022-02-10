# -*- coding: utf-8 -*-
from main_pack.models import Translation
from main_pack.models.Language import Language

def collect_translation_data(
	TranslId = None,
	TranslGuid = None,
	ResCatId = None,
	ColorId = None,
	ProdId = None,
	SlImgId = None,
	LangId = None,
	TranslName = None,
	TranslDesc = None,
	LangName = None,
):

	filtering = {"GCRecord": None}

	if TranslId:
		filtering["TranslId"] = TranslId

	if TranslGuid:
		filtering["TranslGuid"] = TranslGuid

	if ResCatId:
		filtering["ResCatId"] = ResCatId

	if ColorId:
		filtering["ColorId"] = ColorId

	if ProdId:
		filtering["ProdId"] = ProdId

	if SlImgId:
		filtering["SlImgId"] = SlImgId

	if LangId:
		filtering["LangId"] = LangId

	if LangName:
		this_language = Language.query.filter(Language.LangName.ilike(f"%{LangName}%")).first()
		if this_language:
			filtering["LangId"] = this_language.LangId

	db_translations = Translation.query.filter_by(**filtering)

	if TranslName:
		db_translations = db_translations.filter(Translation.TranslName.ilike(f"%{TranslName}%"))

	if TranslDesc:
		db_translations = db_translations.filter(Translation.TranslDesc.ilike(f"%{TranslDesc}%"))


	db_translations = db_translations.all()

	data = [translation_data.to_json_api() for translation_data in db_translations]

	return data