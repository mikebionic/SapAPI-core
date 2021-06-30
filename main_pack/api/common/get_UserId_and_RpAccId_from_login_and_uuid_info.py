from main_pack.models import Rp_acc

def get_UserId_and_RpAccId_from_login_and_uuid_info(
	model_type,
	current_user,
	RpAccGuid = None
):
	user_id, user_short_name, RpAccId, RpAccModel = None, None, None, None

	if model_type == "rp_acc":
		user_id = current_user.user.UId
		user_short_name = current_user.user.UShortName
		RpAccId = current_user.RpAccId
		RpAccModel = current_user

	if model_type == "device":
		current_user = current_user.user
		model_type = "user"

	if model_type == "user":
		user_id = current_user.UId
		user_short_name = current_user.UShortName

		RpAccModel = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
		RpAccId = RpAccModel.RpAccId if RpAccModel else None

	return user_id, user_short_name, RpAccId, RpAccModel