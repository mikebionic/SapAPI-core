# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session
from sqlalchemy.orm import joinedload
from flask_login import login_user
from datetime import datetime
import requests

from main_pack import db
from main_pack.config import Config
from main_pack.api.auth import api
from main_pack.models import User, Rp_acc, Device
from main_pack.api.users.utils import apiUsersData, apiRpAccData, apiDeviceData
from main_pack.api.common.gather_required_register_rp_acc_data import gather_required_register_rp_acc_data

from main_pack.base import generate_random_code
from main_pack.api.base.validators import request_is_json
from main_pack.base import log_print
from main_pack.base.dataMethods import apiDataFormat
from main_pack.base.cryptographyMethods import encodeJWT
from main_pack.base.apiMethods import get_login_info


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
			user_model = register_new_user(auth_type, req)

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
		log_print(f"Google Auth Api exception {ex}")

	return make_response(*error_response)


def check_google_token(token):
	server_response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}").json()
	if 'locale' in server_response:
		session['language'] = server_response['locale']
		return True
	return False


def register_new_user(auth_type, req, random_password=1):
	user_model, message = None, ''
	try:
		if auth_type == "rp_acc":
			rp_acc_data = {
				"RpAccEMail": req['email'],
				"RpAccName": req['fullName'],
				"RpAccUName": req['username'],
				"RpAccFirstName": req['firstName'],
				"RpAccLastName": req['lastName'],
				"AddInf1": req['googleId'],
				"AddInf2": req['imageUrl'],
				"RpAccTypeId": 2,
				"RpAccStatusId": 1,
			}
			if random_password:
				rp_acc_data["RpAccUPass"] = f"{Config.COMPANY_NAME}{generate_random_code()}"

			if not rp_acc_data["RpAccUPass"]:
				message = "Password not valid!"
				log_print(message, "warning")
				raise Exception

			UId, CId, DivId, RpAccRegNo, RpAccGuid = gather_required_register_rp_acc_data()
			rp_acc_data["UId"] = UId
			rp_acc_data["CId"] = CId
			rp_acc_data["DivId"] = DivId
			rp_acc_data["RpAccRegNo"] = RpAccRegNo
			rp_acc_data["RpAccGuid"] = RpAccGuid

			if not rp_acc_data["RpAccName"]:
				rp_acc_data["RpAccName"] = rp_acc_data["RpAccUName"]

			if Config.INSERT_LAST_ID_MANUALLY:
				try:
					lastUser = Rp_acc.query.with_entities(Rp_acc.RpAccId).order_by(Rp_acc.RpAccId.desc()).first()
					RpAccId = lastUser.RpAccId + 1
				except:
					RpAccId = None
				rp_acc_data["RpAccId"] = RpAccId

			user_model = Rp_acc(**rp_acc_data)
			db.session.add(user_model)

			try:
				login_info = get_login_info(request)
				user_model.RpAccLastActivityDate = login_info["date"]
				user_model.RpAccLastActivityDevice = login_info["info"]
			except Exception as ex:
				log_print(f"Rp_acc activity info update Exception: {ex}")

		db.session.commit()
	except Exception as ex:
		log_print(f"Register google User exception {ex}")

	return user_model