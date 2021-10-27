# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session
from sqlalchemy.orm import joinedload
from flask_login import login_user

from main_pack.api.auth import api
from main_pack.models import User, Rp_acc, Device

from main_pack.api.users.utils import apiUsersData, apiRpAccData, apiDeviceData
from main_pack.base.dataMethods import apiDataFormat
from main_pack.api.auth.auth_utils import check_auth
from main_pack.base.cryptographyMethods import encodeJWT
from main_pack.api.common import configurePhoneNumber
from main_pack.base import log_print


@api.route('/login/',methods=['GET','POST'])
def api_login():
	login_method = request.args.get("method","username",type=str)
	auth_type = request.args.get("type","user",type=str)
	auth = request.authorization
	error_response = [{"message": "Login failure, check credentials.", "status": 0}, 401, {"WWW-Authenticate": "basic realm"}]

	try:
		if not auth or not auth.username:
			log_print("API LOGIN not auth or auth.username")
			raise Exception

		user_model, user_query = None, None
		user_query_filter = {"GCRecord": None}

		if auth_type == "user":
			if login_method == "username":
				user_query_filter["UName"] = auth.username
			elif login_method == "email":
				user_query_filter["UEmail"] = auth.username

			user_query = User.query.filter_by(**user_query_filter)

		elif auth_type == "rp_acc":
			if login_method == "username":
				user_query_filter["RpAccUName"] = auth.username
			elif login_method == "email":
				user_query_filter["RpAccEMail"] = auth.username
			elif login_method == "phone_number":
				phone_number = configurePhoneNumber(auth.username)
				if not phone_number:
					log_print("not auth or auth.username")
					raise Exception
				user_query_filter["RpAccMobilePhoneNumber"] = phone_number

			user_query = Rp_acc.query.filter_by(**user_query_filter)

		elif auth_type == "device":
			user_query_filter["DevUniqueId"] = auth.username
			user_query = Device.query\
				.filter_by(**user_query_filter)\
				.options(joinedload(Device.user))

		user_model = user_query.first() if user_query else None

		if not user_model:
			log_print("API LOGIN couldn't find db model")
			raise Exception

		if check_auth(auth_type, user_model, auth.password):
			token_encoding_data = {}

			if auth_type == "user":
				token_encoding_data["UId"] = user_model.UId
				loggedUserInfo = apiUsersData(dbQuery = user_query)

			elif auth_type == "rp_acc":
				token_encoding_data["RpAccId"] = user_model.RpAccId
				loggedUserInfo = apiRpAccData(dbQuery = user_query)

			elif auth_type == "device":
				token_encoding_data["DevId"] = user_model.DevId
				loggedUserInfo = apiDeviceData(dbQuery = user_query)

			token, exp = encodeJWT(token_encoding_data)
			response_data = {"exp": apiDataFormat(exp)}
			response_data[auth_type] = loggedUserInfo['data']
			response_data["token"] = token.decode('UTF-8')
			response_data["message"] = "Login success!"
			response_data["status"] = 1

			session["model_type"] = auth_type
			session["ResPriceGroupId"] = user_model.ResPriceGroupId if auth_type != "device" else None
			if (auth_type == "device"):
				session["ResPriceGroupId"] = user_model.user.ResPriceGroupId if user_model.user else None

			login_user(user_model)
			response_headers = {
				"Authorization": f"Bearer {token.decode('UTF-8')}"
			}
			return make_response(response_data), response_headers

	except Exception:
		pass
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
		token_encoding_data = {"UId": user.UId}
		token, exp = encodeJWT(token_encoding_data)
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
		token_encoding_data = {"RpAccId": rp_acc.RpAccId}
		token, exp = encodeJWT(token_encoding_data)
		rpAccData = apiRpAccData(dbQuery = user_query)
		session["ResPriceGroupId"] = rp_acc.ResPriceGroupId
		return jsonify({
			"token": token.decode('UTF-8'),
			"rp_acc": rpAccData['data'],
			"exp": apiDataFormat(exp)
			})

	return make_response(*error_response)