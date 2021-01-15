# -*- coding: utf-8 -*-
from flask import json,jsonify,request,make_response,abort,session
from sqlalchemy import and_
from datetime import datetime
import datetime as dt
import jwt
from functools import wraps
from main_pack.config import Config

from main_pack.api.auth import api
from main_pack.models.users.models import Users, Rp_acc
from main_pack.api.auth.utils import check_auth
from main_pack.api.users.utils import apiUsersData, apiRpAccData
from main_pack.base.dataMethods import apiDataFormat


def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({"message": "Token is missing!"}), 401
		try:
			data = jwt.decode(token, Config.SECRET_KEY)
			if 'UId' in data:
				model_type = 'Users'
				current_user = Users.query\
					.filter_by(GCRecord = None, UId = data['UId'])\
					.first()
			elif 'RpAccId' in data:
				model_type = 'Rp_acc'
				current_user = Rp_acc.query\
					.filter_by(GCRecord = None, RpAccId = data['RpAccId'])\
					.first()
			user = {
				"model_type": model_type,
				"current_user": current_user
			}
		except Exception as ex:
			return jsonify({"message": "Token is invalid!"}), 401
		return f(user,*args,**kwargs)

	return decorated


@api.route('/login/',methods=['GET','POST'])
def api_login():
	auth_type = request.args.get("type","user",type=str)
	auth = request.authorization
	error_response = [{"error": "Login failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]

	if not auth or not auth.username or not auth.password:
		return make_response(*error_response)

	if auth_type == "user":
		user_query = Users.query.filter_by(GCRecord = None, UName = auth.username)
		user_model = user_query.first()

	elif auth_type == "rp_acc":
		user_query = Rp_acc.query.filter_by(GCRecord = None, RpAccUName = auth.username)
		user_model = user_query.first()

	if not user_model:
		return make_response(*error_response)
	
	if check_auth(auth_type, auth.username, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = 30)
		response_data = {"exp": apiDataFormat(exp)}

		if auth_type == "user":
			token = jwt.encode({"UId": user_model.UId, "exp": exp}, Config.SECRET_KEY)
			loggedUserInfo = apiUsersData(dbQuery = user_query)

		elif auth_type == "rp_acc":
			token = jwt.encode({"RpAccId": user_model.RpAccId, "exp": exp}, Config.SECRET_KEY)
			loggedUserInfo = apiRpAccData(dbQuery = user_query)
		
		response_data[auth_type] = loggedUserInfo['data']
		response_data["token"] = token.decode('UTF-8')
		session["ResPriceGroupId"] = user_model.ResPriceGroupId

		return jsonify(response_data)
	
	return make_response(*error_response)


# !!! route should be kept till update process complete
@api.route('/login/users/',methods=['GET','POST'])
def api_login_users():
	error_response = [{"error": "Login failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response(*error_response)

	user_query = Users.query.filter_by(GCRecord = None, UName = auth.username)
	user = user_query.first()

	if not user:
		return make_response(*error_response)

	if check_auth("user", auth.username, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = 30)
		token = jwt.encode({"UId": user.UId, "exp": exp}, Config.SECRET_KEY)
		userData = apiUsersData(dbQuery = user_query)
		session["ResPriceGroupId"] = user.ResPriceGroupId
		return jsonify({
			"token": token.decode('UTF-8'),
			"user": userData['data'],
			"exp": apiDataFormat(exp)
			})

	return make_response(*error_response)


# !!! route should be kept till update process complete
@api.route('/login/rp-accs/',methods=['GET','POST'])
def api_login_rp_accs():
	error_response = [{"error": "Login failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response(*error_response)

	user_query = Rp_acc.query.filter_by(GCRecord = None, RpAccUName = auth.username)
	rp_acc = user_query.first()

	if not rp_acc:
		return make_response(*error_response)

	if check_auth("rp_acc", auth.username, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = 30)
		token = jwt.encode({"RpAccId": rp_acc.RpAccId, "exp": exp}, Config.SECRET_KEY)
		rpAccData = apiRpAccData(dbQuery = user_query)
		session["ResPriceGroupId"] = rp_acc.ResPriceGroupId
		return jsonify({
			"token": token.decode('UTF-8'),
			"rp_acc": rpAccData['data'],
			"exp": apiDataFormat(exp)
			})

	return make_response(*error_response)


def sha_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({"message": "Token is missing!"}), 401
		
		if token != Config.SYNCH_SHA:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(*args,**kwargs)

	return decorated