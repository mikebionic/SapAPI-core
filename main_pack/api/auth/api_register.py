# -*- coding: utf-8 -*-
from main_pack.base.dataMethods import apiDataFormat
from main_pack.base.apiMethods import get_login_info
from main_pack.api.common.gather_required_register_rp_acc_data import gather_required_register_rp_acc_data
from flask_login import login_user
from main_pack.base.log_print import log_print
from main_pack.api.auth.utils import register_token_required
from flask import jsonify, request, make_response, session
from datetime import datetime
import datetime as dt
import jwt

from main_pack import db
from main_pack.api.auth import api
from main_pack.config import Config
from main_pack.models import Rp_acc

from main_pack.api.users.utils import addRpAccDict, apiRpAccData


@api.route('/register/',methods=['POST'])
@register_token_required
def api_register(token_data):
	register_method = request.args.get("method","email",type=str)
	auth_type = request.args.get("type","user",type=str)

	error_response = [{"error": "Register failure, check credentials."}, 401, {"WWW-Authenticate": "basic realm"}]

	try:
		if not token_data:
			raise Exception

		req = request.get_json()
		rp_acc_data = addRpAccDict(req)

		if not rp_acc_data["RpAccUPass"]:
			log_print("Register api exception, password not valid", "warning")
			raise Exception

		if register_method == "phone-number" and auth_type == "rp_acc":
			UId, CId, DivId, RpAccRegNo, RpAccGuid = gather_required_register_rp_acc_data()
			rp_acc_data["UId"] = UId
			rp_acc_data["CId"] = CId
			rp_acc_data["DivId"] = DivId
			rp_acc_data["RpAccRegNo"] = RpAccRegNo
			rp_acc_data["RpAccGuid"] = RpAccGuid
			rp_acc_data["RpAccTypeId"] = 2
			rp_acc_data["RpAccStatusId"] = 1

		if register_method == "email" and not Config.INSERT_PHONE_NUMBER_ON_REGISTER:
			rp_acc_data["RpAccMobilePhoneNumber"] = None
			rp_acc_data["RpAccEmail"] = token_data["email"]
			rp_acc_data["RpAccUame"] = token_data["username"]

		if register_method == "phone-number" and not Config.INSERT_EMAIL_ON_REGISTER:
			rp_acc_data["RpAccEMail"] = None
			rp_acc_data["RpAccMobilePhoneNumber"] = token_data["phone_number"]

		if Config.INSERT_LAST_ID_MANUALLY:
			lastUser = Rp_acc.query.order_by(Rp_acc.RpAccId.desc()).first()
			RpAccId = lastUser.RpAccId + 1
			rp_acc_data["RpAccId"] = RpAccId

		user_model = Rp_acc(**rp_acc_data)
		db.session.add(user_model)

		try:
			login_info = get_login_info(request)
			user_model.RpAccLastActivityDate = login_info["date"]
			user_model.RpAccLastActivityDevice = login_info["info"]
		except Exception as ex:
			print(f"{datetime.now()} | Rp_acc activity info update Exception: {ex}")
		db.session.commit()

		exp = datetime.now() + dt.timedelta(minutes = Config.TOKEN_EXP_TIME_MINUTES)
		if auth_type == "rp_acc":
			token = jwt.encode({"RpAccId": user_model.RpAccId, "exp": exp}, Config.SECRET_KEY)
			loggedUserInfo = apiRpAccData(dbModel=user_model)

		response_data = {"exp": apiDataFormat(exp)}
		response_data[auth_type] = loggedUserInfo['data']
		response_data["token"] = token.decode('UTF-8')

		session["model_type"] = "rp_acc"
		session["ResPriceGroupId"] = user_model.ResPriceGroupId

		login_user(user_model)
		return jsonify(response_data)

	except Exception as ex:
		log_print(f"API register exception {ex}")


	return make_response(*error_response)
