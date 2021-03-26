# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack.models.base.models import Warehouse
from main_pack import db
from main_pack.base import get_id_from_list_indexing
from main_pack.api.common import (
	get_division_id_guid_list,
	get_CId_WhGuid_list,
)
from .add_Warehouse_dict import add_Warehouse_dict


def save_warehouse_synch_data(req):
	DivId_list, DivGuid_list = get_division_id_guid_list()
	CId_list, DivGuid_list = get_CId_WhGuid_list()

	data, fails = [], []
	for warehouse_req in req:
		try:
			DivGuid = warehouse_req['DivGuid']
			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, warehouse_req['DivGuid'])
			CId = get_id_from_list_indexing(CId_list, DivGuid_list, warehouse_req['DivGuid'])

			if not CId or not DivId:
				raise Exception

			warehouse_info = add_Warehouse_dict(warehouse_req)
			warehouse_info['DivId'] = DivId
			warehouse_info['CId'] = CId

			warehouse = Warehouse.query\
				.filter_by(
					WhGuid = warehouse_info['WhGuid'])\
				.first()

			if warehouse:
				warehouse_info['WhId'] = warehouse.WhId
				warehouse.update(**warehouse_info)
			else:
				warehouse = Warehouse(**warehouse_info)
				db.session.add(warehouse)

			data.append(warehouse_req)

		except Exception as ex:
			print(f"{datetime.now()} | Warehouse Api Exception: {ex}")
			fails.append(warehouse_req)

	db.session.commit()
	return data, fails