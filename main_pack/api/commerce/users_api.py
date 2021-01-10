# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.users import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.base.models import Division,Company
from main_pack.models.users.models import Users
from main_pack.api.users.utils import addUsersDict,apiUsersData
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-users/<UId>/",methods=['GET'])
@sha_required
def api_users_user(UId):
	user = apiUsersData(UId)
	res = {
		"status": 1,
		"message": "Single user",
		"data": user["data"],
		"total": 1
	}
	response = make_response(jsonify(res),200)

	return response


@api.route("/tbl-dk-users/",methods=['GET','POST'])
@sha_required
def api_users():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		users = Users.query.filter_by(GCRecord = None)
		if DivId:
			users = users.filter_by(DivId = DivId)
		if notDivId:
			users = users.filter(Users.DivId != notDivId)
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			users = users.filter(Users.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		users = users.all()

		data = []
		for user in users:
			user_info = user.to_json_api()
			user_info["DivGuid"] = user.division.DivGuid if user.division else None
			user_info["CGuid"] = user.company.CGuid if user.company else None
	
		res = {
			"status": 1,
			"message": "All users",
			"data": data,
			"total": len(users)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
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

			users = []
			failed_users = [] 
			for user_req in req:
				user_info = addUsersDict(user_req)
				try:
					URegNo = user_info["URegNo"]
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

					thisUser = Users.query\
						.filter_by(
							URegNo = URegNo,
							UGuid = UGuid,
							GCRecord = None)\
						.first()
					if thisUser:
						user_info["UId"] = thisUser.UId
						thisUser.update(**user_info)
						users.append(user_req)
					else:
						thisUser = Users(**user_info)
						db.session.add(thisUser)
						users.append(user_req)
						thisUser = None
				except Exception as ex:
					print(f"{datetime.now()} | Users Api Exception: {ex}")
					failed_users.append(user_req)
			db.session.commit()
			status = checkApiResponseStatus(users,failed_users)
			res = {
				"data": users,
				"fails": failed_users,
				"success_total": len(users),
				"fail_total": len(failed_users)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),201)
	return response