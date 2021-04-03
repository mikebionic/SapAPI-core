# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import db
from main_pack.models import (
	Invoice,
	Inv_line,
	Resource
)
from main_pack.api.common import (
	get_division_id_guid_list,
	get_warehouse_id_guid_list,
	get_rp_acc_id_guid_list,
)
from .add_Inv_dict import add_Inv_dict
from .add_Inv_line_dict import add_Inv_line_dict
from main_pack.base import get_id_from_list_indexing

def save_invoice_synch_data(req):
	DivId_list, DivGuid_list = get_division_id_guid_list()
	WhId_list, WhGuid_list = get_warehouse_id_guid_list()
	RpAccId_list, RpAccGuid_list = get_rp_acc_id_guid_list()

	data, fails = [], [] 

	for inv_req in req:
		try:
			invoice_data = add_Inv_dict(inv_req)
			InvRegNo = invoice_data['InvRegNo']
			
			DivGuid = inv_req['DivGuid']
			WhGuid = inv_req['WhGuid']
			RpAccGuid = inv_req['RpAccGuid']

			InvGuid = invoice_data['InvGuid']
			InvRegNo = invoice_data['InvRegNo']

			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, DivGuid)
			WhId = get_id_from_list_indexing(WhId_list, WhGuid_list, WhGuid)
			RpAccId = get_id_from_list_indexing(RpAccId_list, RpAccGuid_list, RpAccGuid)

			invoice_data['DivId'] = DivId
			invoice_data['WhId'] = WhId
			invoice_data['RpAccId'] = RpAccId

			thisInv = Invoice.query\
				.filter_by(
					InvGuid = InvGuid,
					InvRegNo = InvRegNo,
					GCRecord = None)\
				.first()

			if not RpAccId or not DivId or not WhId:
				print(f"{RpAccId}, {DivId}, {WhId}")
				raise Exception

			if thisInv:
				invoice_data['OInvId'] = thisInv.OInvId
				thisInv.update(**invoice_data)
				db.session.commit()

			else:
				thisInv = Invoice(**invoice_data)
				db.session.add(thisInv)
				db.session.commit()

			inv_lines, failed_inv_lines = [], []

			for inv_line_req in invoice_data['inv_lines']:
				inv_line_data = add_Inv_line_dict(inv_line_req)
				inv_line_data['InvId'] = thisInv.InvId

				ResRegNo = inv_line_req['ResRegNo']
				ResGuid = inv_line_req['ResGuid']

				this_line_resource = Resource.query\
					.filter_by(
						ResRegNo = ResRegNo,
						ResGuid = ResGuid,
						GCRecord = None)\
					.first()

				try:
					inv_line_data["ResId"] = this_line_resource.ResId
					InvLineRegNo = inv_line_data['InvLineRegNo']
					InvLineGuid = inv_line_data['InvLineGuid']
					
					thisInvLine = Inv_line.query\
						.filter_by(
							InvLineRegNo = InvLineRegNo,
							InvLineGuid = InvLineGuid,
							GCRecord = None)\
						.first()

					if thisInvLine:
						inv_line_data["InvLineId"] = thisInvLine.InvLineId
						thisInvLine.update(**inv_line_data)

					else:
						thisInvLine = Invoice(**inv_line_data)
						db.session.add(thisInvLine)
						thisInvLine = None
					
					db.session.commit()
					inv_lines.append(inv_line_req)

				except Exception as ex:
					print(f"{datetime.now()} | Inv Api OInvLine Exception: {ex}")
					failed_inv_lines.append(inv_line_req)

			invoice_data['Inv_lines'] = inv_lines
			data.append(invoice_data)

		except Exception as ex:
			print(f"{datetime.now()} | Inv Api Exception: {ex}")
			fails.append(invoice_data)

	return data, fails