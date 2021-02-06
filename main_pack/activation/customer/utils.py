# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from main_pack.config import Config
from main_pack.models.base.models import Db_inf
from main_pack.base.cryptographyMethods import decrypt_data
from main_pack.activation.customer.device_fetch import fetch_device

def check_device_activation(device_model):

	state = False
	do_fetch = False

	database_inf = Db_inf.query.first()
	DbInfGuid = database_inf.DbInfGuid

	DevVerifyKey = device_model.DevVerifyKey

	DevVerifyDate = device_model.DevVerifyDate
	DevVerifyDate = str(DevVerifyDate.replace(tzinfo=timezone.utc).timestamp())

	server_key = Config.BASE_32_FERNET_KEY
	client_key = Config.APP_WEB_KEY

	decrypted_data = decrypt_data(
		data = DevVerifyKey,
		server_key = server_key,
		db_guid = DbInfGuid,
		client_key = client_key
	)

	if not decrypt_data:
		do_fetch = True

	if decrypt_data:
		if (DevVerifyDate == decrypt_data):
			state = True

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

	if current_device["IsAllowed"]:
		state = True

	return state