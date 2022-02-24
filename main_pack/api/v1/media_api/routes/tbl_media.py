# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.media_api import api
from main_pack.api.v1.media_api.utils import collect_media_data
from main_pack.api.v1.media_api.utils.data.save_media_data import save_media_data
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.models import Media
from main_pack.models import Rp_acc
from main_pack.api.common.send_email_message import send_email_message


@api.route("/tbl-media/", methods=['GET'])
def tbl_media_get():
	arg_data = {
		"MediaId": request.args.get("id",None,type=int),
		"MediaTitle": request.args.get("title","",type=str),
		"MediaName": request.args.get("name","",type=str),
		"MediaBody": request.args.get("body","",type=str),
		"MediaAuthor": request.args.get("author","",type=str),
		"MediaIsFeatured": request.args.get("isFeatured",None,type=int),
		"MediaCatId": request.args.get("categoryId",None,type=int),
		"LangName": request.args.get("language","",type=str),
		"startDate": request.args.get("startDate","",type=str),
		"endDate": request.args.get("endDate","",type=str),
	}

	data = collect_media_data(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Media",
		"data": data,
		"total": len(data)
	}
	return make_response(jsonify(res), 200)

@api.route("/tbl-media/", methods=['POST'])
@request_is_json(request)
def tbl_media_post():

	req = request.get_json()

	data, fails = save_media_data(req)
	status = checkApiResponseStatus(data, fails)

	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails),
	}
	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)


@api.route("/send_as_email/")
def send_as_email():
	status = 1
	message = "Mails sent"
	MediaGuid = request.args.get('uuid', '', type=str)
	try:
		if not MediaGuid:
			message = "uuid not passed"
			raise Exception

		selected_media = Media.query.filter_by(MediaGuid = MediaGuid).first()
		if not selected_media:
			message = "media not found"
			raise Exception

		emails = Rp_acc.get_emails(skipNulls = 1)
		message_title = Media.MediaTitle
		message_body = f'''
			{Media.MediaTitle}
			______
			{Media.MediaBody}
			--
			{Media.MediaAuthor}
		'''
		send_email_message(emails, message_title, message_body)

	except Exception as ex:
		status = 0
		message = "err.."
		print(f"Media send as email exception {ex}")
		

	return make_response(jsonify({"status": status, "message": message}), 200)