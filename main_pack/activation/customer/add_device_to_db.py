from datetime import datetime

from main_pack import db
from main_pack.api.users.utils import addDeviceDict
from main_pack.models import Device


def add_device_to_db(payload, dbModel = None):
	try:
		if not payload:
			raise Exception

		device_data = addDeviceDict(payload)
		device_data["RpAccId"] = None

		if dbModel:
			dbModel.update(**device_data)

		else:
			dbModel = Device(**device_data)
			db.session.add(dbModel)

		db.session.commit()
		data = dbModel.to_json_api()

	except Exception as ex:
		print(f"{datetime.now()} | Device register db insertion Exception: {ex}")

	return data