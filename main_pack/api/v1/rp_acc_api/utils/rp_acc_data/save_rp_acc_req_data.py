# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from main_pack import db, bcrypt

from main_pack.models import Rp_acc
from .add_Rp_acc_dict import add_Rp_acc_dict
from main_pack.key_generator.utils import makeRegNo, generate


def save_rp_acc_req_data(req, model_type, current_user, session = None):

	if model_type == "device":
		current_user = current_user.user
		model_type = "user"

	if model_type == "user":
		user_id = current_user.UId
		user_short_name = current_user.UShortName

	DivId = current_user.DivId
	CId = current_user.CId
	UId = current_user.UId

	data, fails = [], []
	for rp_acc_req in req:
		try:
			rp_acc_info = add_Rp_acc_dict(rp_acc_req)

			rp_acc_info["DivId"] = DivId
			rp_acc_info["CId"] = CId
			rp_acc_info["UId"] = UId

			RpAccRegNo = rp_acc_info["RpAccRegNo"]
			RpAccGuid = rp_acc_info["RpAccGuid"]

			if Config.HASHED_PASSWORDS == True:
				rp_acc_info["RpAccUPass"] = bcrypt.generate_password_hash(rp_acc_info["RpAccUPass"]).decode()

			thisRpAcc = Rp_acc.query\
				.filter_by(
					RpAccGuid = RpAccGuid,
					GCRecord = None)\
				.first()

			if thisRpAcc:
				rp_acc_info["RpAccId"] = thisRpAcc.RpAccId
				thisRpAcc.update(**rp_acc_info)

			else:
				try:
					reg_num = generate(UId=current_user.UId,RegNumTypeName='rp_code')
					regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',RegNumTypeName='rp_code')
					reg_num.RegNumLastNum = reg_num.RegNumLastNum + 1
					db.session.commit()
				except Exception as ex:
					print(f"{datetime.now()} | Rp_acc_req save regNo gen Exception: {ex}")
					regNo = str(datetime.now().timestamp())

				rp_acc_info["RpAccRegNo"] = regNo
				rp_acc_info["RpAccGuid"] = uuid.uuid4()
				
				if not rp_acc_info["RpAccUName"]:
					rp_acc_info["RpAccUName"] = f"RpAccUName{datetime.now().timestamp()}"
				if not rp_acc_info["RpAccUPass"]:
					rp_acc_info["RpAccUPass"] = f"RpAccUPass{datetime.now().timestamp()}"

				thisRpAcc = Rp_acc(**rp_acc_info)
				db.session.add(thisRpAcc)
				data.append(thisRpAcc.to_json_api())

			db.session.commit()

		except Exception as ex:
			print(f"{datetime.now()} | v1 Rp_acc Api sych Exception: {ex}")
			fails.append(rp_acc_req)

	return data, fails