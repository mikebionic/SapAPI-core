
from datetime import datetime,timezone
from main_pack.key_generator.utils import generate, makeRegNo
from main_pack.models import Pred_reg_num

def generate_pred_reg_no(req):
	try:
		if model_type == "rp_acc":
			name = current_user.RpAccUName
			RpAccId = current_user.RpAccId
			user = User.query\
				.filter_by(GCRecord = None, UId = current_user.UId)\
				.first()

			if user is None:
				user = User.query\
					.filter_by(GCRecord = None, RpAccId = RpAccId)\
					.first()

		
		RegNumTypeId = req['RegNumTypeId']
		random_mode = req['random_mode']

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