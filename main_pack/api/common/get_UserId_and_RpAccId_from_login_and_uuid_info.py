from main_pack.models import Rp_acc

def get_UserId_and_RpAccId_from_login_and_uuid_info(
	model_type,
	current_user,
	RpAccGuid = None
):
	user_id, user_short_name, RpAccId, RpAccModel, UserModel = None, None, None, None, None

	try:
		if model_type == "rp_acc":
			UserModel = current_user.user
			user_id = UserModel.UId
			user_short_name = UserModel.UShortName
			RpAccId = current_user.RpAccId
			RpAccModel = current_user

		if model_type == "device":
			UserModel = current_user.user
			model_type = "user"

		if model_type == "user":
			user_id = UserModel.UId
			user_short_name = UserModel.UShortName

			RpAccModel = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
			RpAccId = RpAccModel.RpAccId if RpAccModel else None
	except Exception as ex:
		print(f"get_UserId_and_RpAccId exception {ex}")

	return user_id, user_short_name, RpAccId, RpAccModel, UserModel