from main_pack.config import Config

def get_ResPriceGroupId(
	model_type = None,
	current_user= None,
	session = None,
	get_from_current_user = False,
):
	ResPriceGroupId = Config.DEFAULT_RES_PRICE_GROUP_ID if Config.DEFAULT_RES_PRICE_GROUP_ID > 0 else None
	try:
		if current_user:
			if (model_type == "device" and not get_from_current_user):
				ResPriceGroupId = current_user.user.ResPriceGroupId if current_user.user else ResPriceGroupId
			else:
				ResPriceGroupId = current_user.ResPriceGroupId if current_user.ResPriceGroupId else ResPriceGroupId

		elif "ResPriceGroupId" in session:
			ResPriceGroupId = session["ResPriceGroupId"]

	except Exception as ex:
		print(f"ResPriceGroupId {ex}")

	return ResPriceGroupId