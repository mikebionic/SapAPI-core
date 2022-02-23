

from uuid import uuid4

from main_pack.api.v1.translation_api.utils.data.add_Translation_dict import add_Translation_dict
from main_pack.models.Language import Language
from main_pack.models.Res_category import Res_category
from main_pack.models.Translation import Translation
from main_pack import db
from main_pack.base import log_print

def save_translation_data(req):
	data, fails = [], []

	for transl_req in req:
		try:
			this_transl_data = add_Translation_dict(transl_req)

			LangName = transl_req["LangName"]
			if LangName:
				this_language = Language.query.filter(Language.LangName.ilike(f"%{LangName}%")).first()
				if this_language:
					this_transl_data["LangId"] = this_language.LangId
			
			ResCatName = transl_req["ResCatName"]
			if ResCatName:
				this_category = Res_category.query.filter(Res_category.ResCatName.ilike(f"%{ResCatName}%")).first()
				if this_category:
					this_transl_data["ResCatId"] = this_category.ResCatId

			if not this_transl_data["LangId"] or not this_transl_data["ResCatId"]:
				log_print(f"Translations api: No langId or data specified {transl_req}", "warning")
				raise Exception

			this_translation = Translation.query.filter_by(
				LangId = this_transl_data["LangId"],
				ResCatId = this_transl_data["ResCatId"],
			).first()

			if this_translation:
				this_translation.update(**this_transl_data)

			else:
				this_transl_data["TranslGuid"] = uuid4()
				this_translation = Translation(**this_transl_data)
				db.session.add(this_translation)

			data.append(this_translation.to_json_api())

		except Exception as ex:
			log_print(f"Translations api: {ex}")
			fails.append(transl_req)

	db.session.commit()

	return data, fails