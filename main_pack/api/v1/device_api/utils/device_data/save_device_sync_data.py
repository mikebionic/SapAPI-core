# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import db

from main_pack.models import Device, User
from .add_Device_dict import add_Device_dict


def save_device_sync_data(req):
	data, fails = [], []

	for device_req in req:
		try:
			device_info = add_Device_dict(device_req)

			DevUniqueId = device_info["DevUniqueId"]
			DevGuid = device_info["DevGuid"]
			if "UGuid" in device_req:
				UGuid = device_req["UGuid"]
				if UGuid:
					this_user = User.query.filter(User.UGuid == UGuid).first()
					device_info["UId"] = this_user.UId

			thisDevice = Device.query\
				.filter_by(
					DevUniqueId = DevUniqueId,
					DevGuid = DevGuid,
					GCRecord = None)\
				.first()

			if thisDevice:
				device_info["DevId"] = thisDevice.DevId
				thisDevice.update(**device_info)
				data.append(device_req)

			else:
				thisDevice = Device(**device_info)
				db.session.add(thisDevice)
				data.append(device_req)
				thisDevice = None

		except Exception as ex:
			print(f"{datetime.now()} | v1 Device Api synch Exception: {ex}")
			fails.append(device_req)

	try:
		db.session.commit()
	except Exception as ex:
		print(f"{datetime.now()} | v1 Device Api synch Exception: {ex}")

	return data, fails