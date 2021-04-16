# -*- coding: utf-8 -*-
from sqlalchemy.orm import joinedload
import dateutil.parser
from datetime import datetime, timedelta

from main_pack.models import User
from main_pack.base.apiMethods import fileToURL


def collect_user_data(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	UId = None,
	URegNo = None,
	UName = None,
	withPassword = 0,
	withImage = 0,
):

	filtering = {"GCRecord": None}

	if UId:
		filtering["UId"] = UId
	if URegNo:
		filtering["URegNo"] = URegNo
	if UName:
		filtering["UName"] = UName
	if DivId:
		filtering["DivId"] = DivId

	users = User.query.filter_by(**filtering)\
		.options(
			joinedload(User.company),
			joinedload(User.division))

	if notDivId:
		users = users.filter(User.DivId != notDivId)

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		users = users.filter(User.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	users = users.all()

	data = []
	for user in users:
		user_info = user.to_json_api()
		user_info["DivGuid"] = user.division.DivGuid if user.division and not user.division.GCRecord else None
		user_info["CGuid"] = user.company.CGuid if user.company and not user.company.GCRecord else None
		data.append(user_info)

		if withImage:
			user_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=user.Image[-1].FileName) if user.Image else ""
			user_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=user.Image[-1].FileName) if user.Image else ""
			user_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=user.Image[-1].FileName) if user.Image else ""

		if withPassword:
			user_info["UPass"] = user.UPass

	return data