# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta

from main_pack.config import Config
from main_pack.models import Db_inf
from main_pack.base.cryptographyMethods import decrypt_data
from main_pack.activation.customer.device_fetch import fetch_device


def check_device_activation(device_model):

	state = False
	do_fetch = False
	current_device = None

	database_inf = Db_inf.query.first()
	DbInfGuid = database_inf.DbInfGuid

	DevVerifyKey = device_model.DevVerifyKey
	DevVerifyDate = device_model.DevVerifyDate

	decrypted_data = decrypt_data(
		data = DevVerifyKey,
		server_key = Config.BASE_32_FERNET_KEY.encode(),
		db_guid = DbInfGuid,
		client_key = Config.APP_WEB_KEY
	)

	if not decrypted_data:
		do_fetch = True

	if decrypted_data:
		if (str(DevVerifyDate.replace(tzinfo=timezone.utc).timestamp()) == decrypted_data):
			if (DevVerifyDate > datetime.today() - timedelta(days = Config.DEVICE_ALLOWED_TIMEOUT_DAYS)):
				state = True

			else:
				do_fetch = True

		else:
			do_fetch = True

	if do_fetch:
		try:
			data = fetch_device()

			for device in data["data"]["Devices"]:
				if (device["DevUniqueId"] == device_model.DevUniqueId):
					current_device = device

		except Exception as ex:
			print(f"{datetime.now()} | Check dev activation exception {ex}")

	else:
		current_device = device_model.to_json_api()

	if current_device:
		if current_device["IsAllowed"]:
			state = True

	return state