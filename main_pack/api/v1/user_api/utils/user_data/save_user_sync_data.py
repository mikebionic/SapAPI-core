# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import db
from main_pack.api.common import (
	get_company_id_guid_list,
	get_division_id_guid_list,
)
from main_pack.base import get_id_from_list_indexing
from main_pack.models import User
from .add_User_dict import add_User_dict


def save_user_sync_data(req):
	data, fails = [], []

	CId_list, CGuid_list = get_company_id_guid_list()
	DivId_list, DivGuid_list = get_division_id_guid_list()

	for user_req in req:
		try:
			user_info = add_User_dict(user_req)

			URegNo = user_info["URegNo"]
			UGuid = user_info["UGuid"]

			CId = get_id_from_list_indexing(CId_list, CGuid_list, user_req["CGuid"])
			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, user_req["DivGuid"])

			if not DivId or not CId:
				raise Exception

			user_info["CId"] = CId
			user_info["DivId"] = DivId

			if not user_info["UPass"]:
				print(f'{user_info["UName"]} has no password, skipping...')
				raise Exception

			thisUser = User.query\
				.filter_by(
					URegNo = URegNo,
					UGuid = UGuid,
					GCRecord = None)\
				.first()

			if thisUser:
				user_info["UId"] = thisUser.UId
				thisUser.update(**user_info)
				data.append(user_req)

			else:
				thisUser = User(**user_info)
				db.session.add(thisUser)
				data.append(user_req)
				thisUser = None

		except Exception as ex:
			print(f"{datetime.now()} | v1 User Api synch Exception: {ex}")
			fails.append(user_req)

	try:
		db.session.commit()
	except Exception as ex:
		print(f"{datetime.now()} | v1 User Api synch Exception: {ex}")

	return data, fails