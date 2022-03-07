# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import db

from main_pack.models import Resource
from .add_resource_dict import add_resource_dict


def save_resource_sync_data(req):
	data, fails = [], []

	for resource_req in req:
		try:
			resource_info = add_resource_dict(resource_req)

			DevUniqueId = resource_info["DevUniqueId"]
			DevGuid = resource_info["DevGuid"]

			thisresource = Resource.query\
				.filter_by(
					DevUniqueId = DevUniqueId,
					DevGuid = DevGuid,
					GCRecord = None)\
				.first()

			if thisresource:
				resource_info["DevId"] = thisresource.DevId
				thisresource.update(**resource_info)
				data.append(resource_req)

			else:
				thisresource = Resource(**resource_info)
				db.session.add(thisresource)
				data.append(resource_req)
				thisresource = None

		except Exception as ex:
			print(f"{datetime.now()} | v1 resource Api synch Exception: {ex}")
			fails.append(resource_req)

	try:
		db.session.commit()
	except Exception as ex:
		print(f"{datetime.now()} | v1 resource Api synch Exception: {ex}")

	return data, fails