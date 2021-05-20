# -*- coding: utf-8 -*-
from datetime import datetime,timezone

from main_pack import db
from main_pack.models import Pred_reg_num
from main_pack.key_generator.utils import generate, makeRegNo


def generate_pred_reg_no(req, model_type, current_user):
	data = None
	try:
		if model_type == "rp_acc":
			user_id = current_user.user.UId
			user_short_name = current_user.user.UShortName
			RpAccId = current_user.RpAccId

		if model_type == "device":
			current_user = current_user.user
			model_type = "user"

		if model_type == "user":
			user_id = current_user.UId
			user_short_name = current_user.UShortName

		RegNumTypeId = req['RegNumTypeId'] if 'RegNumTypeId' in req else None
		random_mode = req['random_mode'] if 'random_mode' in req else None
		RegNumTypeName = req['RegNumTypeName'] if 'RegNumTypeName' in req else None

		try:
			reg_num = generate(
				UId = user_id,
				RegNumTypeId = RegNumTypeId,
				RegNumTypeName = RegNumTypeName,
			)
			generation_params = {
				"shortName": user_short_name,
				"prefix": reg_num.RegNumPrefix,
				"lastNum": reg_num.RegNumLastNum + 1,
				"RegNumTypeId": RegNumTypeId,
				"RegNumTypeName": RegNumTypeName,
				"random_mode": random_mode,
			}
			currentRegNo = makeRegNo(**generation_params)

		except Exception as ex:
			print(f"{datetime.now()} | Pred Reg_no gen function Exception: {ex}")
			currentRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())

		New_Pred_regnum = Pred_reg_num(RegNum = currentRegNo, RegNumTypeId = RegNumTypeId)
		db.session.add(New_Pred_regnum)
		db.session.commit()

		data = currentRegNo

	except Exception as ex:
		print(f"{datetime.now()} | Pred Reg_no gen function Exception: {ex}")

	return data