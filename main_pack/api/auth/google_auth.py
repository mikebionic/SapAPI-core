# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session
from sqlalchemy.orm import joinedload
from flask_login import login_user
import requests

from main_pack.api.auth import api
from main_pack.models import User, Rp_acc, Device
from main_pack.api.users.utils import apiUsersData, apiRpAccData, apiDeviceData

from main_pack.api.base.validators import request_is_json
from main_pack.base import log_print
from main_pack.base.dataMethods import apiDataFormat
from main_pack.base.cryptographyMethods import encodeJWT


@api.route('/google-auth/', methods=['POST'])
@request_is_json(request)
def google_auth():
	auth_type = request.args.get("type","user",type=str)
	error_response = [{"message": "Login failure, check credentials.", "status": 0}, 401, {"WWW-Authenticate": "basic realm"}]
	user_model, user_query = None, None
	req = request.get_json()

	try:
		if not check_google_token(req['accessToken']):
			raise Exception
		user_query_filter = {"GCRecord": None}

		if auth_type == "user":
			user_query_filter["UEmail"] = req['email']
			user_query = User.query.filter_by(**user_query_filter)

		elif auth_type == "rp_acc":
			user_query_filter["RpAccEMail"] = req['email']
			user_query = Rp_acc.query.filter_by(**user_query_filter)

		user_model = user_query.first() if user_query else None

		if not user_model:
			log_print("API LOGIN couldn't find db model")
			log_print("Here should be a profile creation")
			raise Exception

		if user_model:
			token_encoding_data = {}

			if auth_type == "user":
				token_encoding_data["UId"] = user_model.UId
				loggedUserInfo = apiUsersData(dbQuery = user_query)

			elif auth_type == "rp_acc":
				token_encoding_data["RpAccId"] = user_model.RpAccId
				loggedUserInfo = apiRpAccData(dbQuery = user_query)

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

	except Exception as ex:
		print(ex)
		pass
	return make_response(*error_response)


def check_google_token(token):
	server_response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}").json()
	print(server_response)
	if 'email' in server_response:
		session['language'] = ['locale']
		return True
	return False