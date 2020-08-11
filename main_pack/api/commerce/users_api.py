# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.users import api
from main_pack.base.apiMethods import checkApiResponseStatus

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
		"data": user['data'],
		"total": 1
	}
	response = make_response(jsonify(res),200)

	return response

@api.route("/tbl-dk-users/",methods=['GET','POST'])
@sha_required
def api_users():
	if request.method == 'GET':
		users = Users.query.all()
		res = {
			"status": 1,
			"message": "All users",
			"data": [user.to_json_api() for user in users],
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
			users = []
			failed_users = [] 
			for user in req:
				user = addUsersDict(user)
				try:
					if not 'UId' in user:
						newOrderInv = Users(**user)
						db.session.add(newOrderInv)
						db.session.commit()
						users.append(user)
					else:
						UId = user['UId']
						thisOrderInv = Users.query.get(int(UId))
						if thisOrderInv is not None:
							thisOrderInv.update(**user)
							db.session.commit()
							users.append(user)

						else:
							newOrderInv = Users(**user)
							db.session.add(newOrderInv)
							db.session.commit()
							users.append(user)
				except Exception as ex:
					print(ex)
					failed_users.append(user)

			status = checkApiResponseStatus(users,failed_users)
			res = {
				"data": users,
				"fails": failed_users,
				"success_total": len(users),
				"fail_total": len(failed_users)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),201)
	return response