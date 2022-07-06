

from uuid import uuid4

from main_pack.api.v1.translation_api.utils.data.add_Translation_dict import add_Res_translation_dict
from main_pack.models import Language, Res_translation, Resource
from main_pack import db
from main_pack.base import log_print

def save_res_translation_data(req):
	data, fails = [], []

	for transl_req in req:
		try:
			this_transl_data = add_Res_translation_dict(transl_req)

			LangName = transl_req["LangName"]
			if LangName:
				this_language = Language.query.filter(Language.LangName.ilike(f"%{LangName}%")).first()
				if this_language:
					this_transl_data["LangId"] = this_language.LangId
			
			ResGuid = transl_req["ResGuid"]
			if ResGuid:
				this_resource = Resource.query.filter(Resource.ResGuid == ResGuid).first()
				if this_resource:
					this_transl_data["ResId"] = this_resource.ResId

			if not this_transl_data["LangId"] or not this_transl_data["ResId"]:
				log_print(f"Translations api: No langId or data specified {transl_req}", "warning")
				raise Exception

			this_translation = Res_translation.query.filter_by(
				LangId = this_transl_data["LangId"],
				ResId = this_transl_data["ResId"],
			).first()

			if this_translation:
				this_translation.update(**this_transl_data)

			else:
				this_transl_data["ResTranslGuid"] = uuid4()
				this_translation = Res_translation(**this_transl_data)
				db.session.add(this_translation)

			data.append(this_translation.to_json_api())

		except Exception as ex:
			log_print(f"Translations api: {ex}")
			fails.append(transl_req)

	db.session.commit()

	return data, fails