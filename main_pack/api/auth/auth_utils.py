# -*- coding: utf-8 -*-
from main_pack.config import Config
from main_pack.models.users.models import Users, Rp_acc, Device
from main_pack.activation.customer.utils import check_device_activation


def check_auth(auth_type, user_model, password):
	auth_status = False

	if (auth_type == "user"):

		if Config.HASHED_PASSWORDS == True:
			auth_status = bcrypt.check_password_hash(user_model.UPass, password)
		else:
			auth_status = (user_model.UPass == password)

	elif (auth_type == "rp_acc"):

		if Config.HASHED_PASSWORDS == True:
			auth_status = bcrypt.check_password_hash(user_model.RpAccUPass, password)
		else:
			auth_status = (user_model.RpAccUPass == password)

	elif (auth_type == "device"):
		if check_device_activation(device_model = user_model):
			auth_status = True

	return auth_status