# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.base import api
from main_pack.config import Config

from main_pack import db,babel,gettext,lazy_gettext
from datetime import datetime,timezone

from main_pack.models import User
from main_pack.api.auth.utils import token_required

from main_pack.key_generator.utils import generate, makeRegNo
from main_pack.models import Pred_reg_num


@api.route("/gen-reg-no/",methods=['POST'])
@token_required
def api_gen_reg_no(user):
	model_type = user['model_type']
	current_user = user['current_user']
	try:
		# !!! current user is rp_acc if type is rp_acc
		if model_type == "rp_acc":
			name = current_user.RpAccUName
			RpAccId = current_user.RpAccId
			# get the seller's user information of a specific rp_acc
			user = User.query\
				.filter_by(GCRecord = None, UId = current_user.UId)\
				.first()
			if user is None:
				# try to find the rp_acc registered user if no seller specified
				user = User.query\
					.filter_by(GCRecord = None, RpAccId = RpAccId)\
					.first()

		req = request.get_json()
		RegNumTypeId = req['RegNumTypeId']
		random_mode = req['random_mode']

		######## generate reg no ########
		try:
			reg_num = generate(UId=user.UId,RegNumTypeId=RegNumTypeId)
			generation_params = {
				"shortName": user.UShortName,
				"prefix": reg_num.RegNumPrefix,
				"lastNum": reg_num.RegNumLastNum+1,
				"RegNumTypeId": RegNumTypeId,
				"random_mode": random_mode
			}
			currentRegNo = makeRegNo(**generation_params)
		except Exception as ex:
			print(f"{datetime.now()} | Reg_no Api Exception: {ex}")
			currentRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())

		New_Pred_regnum = Pred_reg_num(RegNum = currentRegNo, RegNumTypeId = RegNumTypeId)
		db.session.add(New_Pred_regnum)
		db.session.commit()

		status = 1
		data = currentRegNo
		message = "Generated Reg num"

	except Exception as ex:
		print(f"{datetime.now()} | Reg_no Api Exception: {ex}")
		status = 0
		data = ""
		message = "Failed to generate"

	res = {
		"status": status,
		"data": data,
		"message": message
	}

	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response