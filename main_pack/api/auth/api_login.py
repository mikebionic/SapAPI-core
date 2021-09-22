# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session
from sqlalchemy.orm import joinedload
from datetime import datetime
import datetime as dt
import jwt

from main_pack.api.auth import api
from main_pack.config import Config

from main_pack.models import User, Rp_acc, Device

from main_pack.api.users.utils import apiUsersData, apiRpAccData, apiDeviceData
from main_pack.base.dataMethods import apiDataFormat
from main_pack.api.auth.auth_utils import check_auth


@api.route('/login/',methods=['GET','POST'])
def api_login():
	auth_type = request.args.get("type","user",type=str)
	auth = request.authorization
	error_response = [{"error": "Login failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]

	if not auth or not auth.username:
		return make_response(*error_response)

	user_model = None

	if auth_type == "user":
		user_query = User.query.filter_by(GCRecord = None, UName = auth.username)
		user_model = user_query.first()

	elif auth_type == "rp_acc":
		user_query = Rp_acc.query.filter_by(GCRecord = None, RpAccUName = auth.username)
		user_model = user_query.first()

	elif auth_type == "device":
		user_query = Device.query\
			.filter_by(GCRecord = None, DevUniqueId = auth.username)\
			.options(joinedload(Device.user))
		user_model = user_query.first()

	if not user_model:
		return make_response(*error_response)

	if check_auth(auth_type, user_model, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)
		exputc = datetime.utcnow() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)

		response_data = {"exp": apiDataFormat(exp)}

		token_encoding_data = {
			"exp": exputc,
			"iat": datetime.utcnow(),
			"nbf": datetime.utcnow()
		}

		if auth_type == "user":
			token_encoding_data["UId"] = user_model.UId
			loggedUserInfo = apiUsersData(dbQuery = user_query)

		elif auth_type == "rp_acc":
			token_encoding_data["RpAccId"] = user_model.RpAccId
			loggedUserInfo = apiRpAccData(dbQuery = user_query)

		elif auth_type == "device":
			token_encoding_data["DevId"] = user_model.DevId
			loggedUserInfo = apiDeviceData(dbQuery = user_query)

		token = jwt.encode(token_encoding_data, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
		response_data[auth_type] = loggedUserInfo['data']
		response_data["token"] = token.decode('UTF-8')

		session["ResPriceGroupId"] = user_model.ResPriceGroupId if auth_type != "device" else None
		if (auth_type == "device"):
			session["ResPriceGroupId"] = user_model.user.ResPriceGroupId if user_model.user else None

		return jsonify(response_data)

	return make_response(*error_response)


# !!! route should be kept till update process complete
@api.route('/login/users/',methods=['GET','POST'])
def api_login_users():
	error_response = [{"error": "Login failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response(*error_response)

	user_query = User.query.filter_by(GCRecord = None, UName = auth.username)
	user = user_query.first()

	if not user:
		return make_response(*error_response)

	if check_auth("user", user, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)
		exputc = datetime.utcnow() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)

		token_encoding_data = {
			"exp": exputc,
			"iat": datetime.utcnow(),
			"nbf": datetime.utcnow()
		}

		token_encoding_data["UId"] = user.UId
		token = jwt.encode(token_encoding_data, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
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

	if check_auth("rp_acc", rp_acc, auth.password):
		exp = datetime.now() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)
		exputc = datetime.utcnow() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)

		token_encoding_data = {
			"exp": exputc,
			"iat": datetime.utcnow(),
			"nbf": datetime.utcnow()
		}

		token_encoding_data["RpAccId"] = rp_acc.RpAccId
		token = jwt.encode(token_encoding_data, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
		rpAccData = apiRpAccData(dbQuery = user_query)
		session["ResPriceGroupId"] = rp_acc.ResPriceGroupId
		return jsonify({
			"token": token.decode('UTF-8'),
			"rp_acc": rpAccData['data'],
			"exp": apiDataFormat(exp)
			})

	return make_response(*error_response)