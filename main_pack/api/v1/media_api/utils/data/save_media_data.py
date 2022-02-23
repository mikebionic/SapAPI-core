from uuid import uuid4

from main_pack.api.v1.media_api.utils.data.add_media_dict import add_media_dict
from main_pack.models import Language
from main_pack.models import Media
from main_pack import db
from main_pack.base import log_print


def save_media_data(req):
	data, fails = [], []

	for media_req in req:
		try:
			this_req_data = add_media_dict(media_req)

			LangName = media_req["LangName"]
			if LangName:
				this_language = Language.query.filter(Language.LangName.ilike(f"%{LangName}%")).first()
				if this_language:
					this_req_data["LangId"] = this_language.LangId

			this_media = None
			MediaGuid = this_req_data["MediaGuid"]
			if MediaGuid:
				this_media = Media.query.filter_by(
					MediaGuid = MediaGuid
				).first()

			if this_media:
				this_media.update(**this_req_data)

			else:
				this_req_data["MediaGuid"] = uuid4()
				this_media = Media(**this_req_data)
				db.session.add(this_media)

			data.append(this_media.to_json_api())

		except Exception as ex:
			log_print(f"Media api: {ex}")
			fails.append(media_req)

	db.session.commit()

	return data, fails