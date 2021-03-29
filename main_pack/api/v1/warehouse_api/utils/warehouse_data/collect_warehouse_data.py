# -*- coding: utf-8 -*-
import dateutil.parser
from datetime import datetime
from sqlalchemy.orm import joinedload

from main_pack.models.base.models import Warehouse


def collect_warehouse_data(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	WhId = None,
	WhName = None
):

	filtering = {"GCRecord": None}

	if WhId:
		filtering["WhId"] = WhId
	if WhName:
		filtering["WhName"] = WhName
	if DivId:
		filtering["DivId"] = DivId

	warehouse_query = Warehouse.query.filter_by(**filtering)\
		.options(
			joinedload(Warehouse.company),
			joinedload(Warehouse.division))

	if notDivId:
		warehouse_query = warehouse_query.filter(Warehouse.DivId != notDivId)

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		warehouse_query = warehouse_query.filter(Warehouse.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	warehouses = warehouse_query.all()

	data = []
	for warehouse in warehouses:
		warehouse_info = warehouse.to_json_api()
		warehouse_info["DivGuid"] = warehouse.division.DivGuid if warehouse.division and not warehouse.division.GCRecord else None
		data.append(warehouse_info)

	return data