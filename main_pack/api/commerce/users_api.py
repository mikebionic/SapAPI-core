# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from sqlalchemy.orm import joinedload
import dateutil.parser
from datetime import datetime, timedelta

from main_pack import db
from main_pack.api.users import api

from main_pack.models import Division,Company
from main_pack.models import User
from main_pack.api.users.utils import addUsersDict

from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.utils import sha_required, token_required
from main_pack.api.base.validators import request_is_json


def get_users(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	UId = None,
	URegNo = None,
	UName = None):

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

	return data


@api.route("/device-user/")
@token_required
def api_device_user(user):
	current_user = user["current_user"]

	data = current_user.user.to_json_api() if current_user.user else {}

	res = {
		"status": 1 if data else 0,
		"message": "Device user",
		"data": data,
		"total": 1 if data else 0
	}
	response = make_response(jsonify(res), 200)

	return response

@api.route("/v-users/")
@token_required
def api_v_users(user):
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"UId": request.args.get("id",None,type=int),
		"URegNo": request.args.get("regNo","",type=str),
		"UName": request.args.get("name","",type=str)
	}

	data = get_users(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "User",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/tbl-dk-users/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_users():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"notDivId": request.args.get("notDivId",None,type=int),
			"synchDateTime": request.args.get("synchDateTime",None,type=str),
			"UId": request.args.get("id",None,type=int),
			"URegNo": request.args.get("regNo","",type=str),
			"UName": request.args.get("name","",type=str)
		}

		data = get_users(**arg_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "User",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		divisions = Division.query\
			.filter_by(GCRecord = None)\
			.filter(Division.DivGuid != None).all()
		companies = Company.query\
			.filter_by(GCRecord = None)\
			.filter(Company.CGuid != None).all()

		division_DivId_list = [division.DivId for division in divisions]
		division_DivGuid_list = [str(division.DivGuid) for division in divisions]
		company_CId_list = [company.CId for company in companies]
		company_CGuid_list = [str(company.CGuid) for company in companies]

		data = []
		failed_data = [] 

		for user_req in req:
			user_info = addUsersDict(user_req)
			try:
				URegNo = user_info["URegNo"]
				if not user_info["URegNo"]:
					URegNo = str(datetime.now().timestamp())
					user_info["URegNo"] = URegNo

				user_info["UShortName"] = f'{user_info["UName"][0]}{user_info["UName"][-1]}'.upper()
				UGuid = user_info["UGuid"]
				CGuid = user_req["CGuid"]
				DivGuid = user_req["DivGuid"]

				try:
					indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
					DivId = int(indexed_div_id)
				except:
					DivId = None
				try:
					indexed_c_id = company_CId_list[company_CGuid_list.index(CGuid)]
					CId = int(indexed_c_id)
				except:
					CId = None

				user_info["CId"] = CId
				user_info["DivId"] = DivId
				if not user_info["UPass"]:
					print(f'{user_info["UName"]} has no password, skipping...')
					raise Exception

				thisUser = User.query\
					.filter_by(
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
				print(f"{datetime.now()} | User Api Exception: {ex}")
				failed_data.append(user_req)

		db.session.commit()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response