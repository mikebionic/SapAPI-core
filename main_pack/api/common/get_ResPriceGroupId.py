from main_pack.config import Config

def get_ResPriceGroupId(
	model_type = None,
	current_user= None,
	session = None
):
	ResPriceGroupId = Config.DEFAULT_RES_PRICE_GROUP_ID if Config.DEFAULT_RES_PRICE_GROUP_ID > 0 else None
	if current_user:
		if (model_type == "device"):
			ResPriceGroupId = current_user.user.ResPriceGroupId if current_user.user else None
		else:
			ResPriceGroupId = current_user.ResPriceGroupId if current_user.ResPriceGroupId else None

	elif "ResPriceGroupId" in session:
		ResPriceGroupId = session["ResPriceGroupId"]

	return ResPriceGroupId