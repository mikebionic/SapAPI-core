# -*- coding: utf-8 -*-
import dateutil.parser
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

from main_pack.models import Device


def collect_device_data(
	synchDateTime = None,
	DevId = None,
	RpAccId = None,
	UId = None,
	IsAllowed = None,
	DevUniqueId = None,
	DevName = None,
	withPassword = 0,
):

	filtering = {"GCRecord": None}

	if DevId:
		filtering["DevId"] = DevId
	if RpAccId:
		filtering["RpAccId"] = RpAccId
	if UId:
		filtering["UId"] = UId
	if IsAllowed:
		filtering["IsAllowed"] = True

	devices = Device.query.filter_by(**filtering)

	if DevName:
		devices = devices.filter(Device.DevName.ilike(f"%{DevName}%"))
	if DevUniqueId:
		devices = devices.filter(Device.DevUniqueId.ilike(f"%{DevUniqueId}%"))

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		devices = devices.filter(Device.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	devices = devices.options(joinedload(Device.user))
	devices = devices.all()

	data = []
	for device in devices:
		device_data = device.to_json_api()
		device_data["UName"] = device.user.UName if device.user else ''
		device_data["UFullName"] = device.user.UFullName if device.user else ''
		data.append(device_data)

	return data