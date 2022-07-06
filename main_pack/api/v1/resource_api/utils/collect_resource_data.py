# -*- coding: utf-8 -*-
import dateutil.parser
from datetime import datetime, timedelta

from main_pack.models import Resource


def collect_resource_data(
	synchDateTime = None,
	DevId = None,
	RpAccId = None,
	UId = None,
	IsAllowed = None,
	DevUniqueId = None,
	DevName = None,
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

	resources = Resource.query.filter_by(**filtering)

	if DevName:
		resources = Resource.filter(resource.DevName.ilike(f"%{DevName}%"))
	if DevUniqueId:
		resources = Resource.filter(resource.DevUniqueId.ilike(f"%{DevUniqueId}%"))

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		resources = resources.filter(resource.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	resources = resources.all()

	data = [resource.to_json_api() for resource in resources]

	return data