from flask import request
from main_pack.api.v1.status_api import api
from main_pack.api.response_handlers.handle_default_response import handle_default_response
from main_pack.models import Inv_status

@api.route("/inv-statuses/")
def inv_status_get():
	request_props = {	
		"id": request.args.get("id", None, type=int),
		"uuid": request.args.get("uuid", None, type=str),
		"name": request.args.get("name", None, type=str),
		"name_tk": request.args.get("name_tk", None, type=str),
		"name_ru": request.args.get("name_ru", None, type=str),
		"name_en": request.args.get("name_en", None, type=str),
	}
	dbModels = Inv_status.get_all(**request_props)
	data = [item.to_json_api() for item in dbModels]
	return handle_default_response(data, "Invoice statuses")