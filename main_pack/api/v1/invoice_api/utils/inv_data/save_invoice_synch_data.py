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
	get_company_id_guid_list,
	get_user_id_guid_list,
)
from .add_Inv_dict import add_Inv_dict
from .add_Inv_line_dict import add_Inv_line_dict
from main_pack.base import get_id_from_list_indexing

def save_invoice_synch_data(req, whInv=0):
	DivId_list, DivGuid_list = get_division_id_guid_list()
	WhId_list, WhGuid_list = get_warehouse_id_guid_list()
	RpAccId_list, RpAccGuid_list = get_rp_acc_id_guid_list()
	CId_list, CGuid_list = get_company_id_guid_list()
	UId_list, UGuid_list = get_user_id_guid_list()

	db_Currencies = Currency.query.all()

	data, fails = [], [] 

	for inv_req in req:
		fail_code, fail_message, fail_data = 1, "", None
		try:
			invoice_data = add_Inv_dict(inv_req)
			DivGuid = inv_req['DivGuid']
			WhGuid = inv_req['WhGuid']
			RpAccGuid = inv_req['RpAccGuid']
			CGuid = inv_req['CGuid']
			UGuid = inv_req['UGuid']

			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, DivGuid)
			WhId = get_id_from_list_indexing(WhId_list, WhGuid_list, WhGuid)
			RpAccId = get_id_from_list_indexing(RpAccId_list, RpAccGuid_list, RpAccGuid)
			CId = get_id_from_list_indexing(CId_list, CGuid_list, CGuid)
			UId = get_id_from_list_indexing(UId_list, UGuid_list, UGuid)

			invoice_data['DivId'] = DivId
			invoice_data['WhId'] = WhId
			invoice_data['RpAccId'] = RpAccId
			invoice_data['CId'] = CId
			invoice_data['UId'] = UId
			try:
				invoice_data['CurrencyId'] = [currency.CurrencyId for currency in db_Currencies if currency.CurrencyCode == inv_req["CurrencyCode"]][0]
			except:
				fail_code, fail_message, fail_data = 1, "Currency not found", inv_line_req["CurrencyCode"]

			thisInv = Invoice.query\
				.filter_by(
					InvGuid = invoice_data['InvGuid'],
					InvRegNo = invoice_data['InvRegNo'],
					GCRecord = None)\
				.first()

			if not RpAccId or not DivId or not WhId:
				if not RpAccId:
					fail_code, fail_message, fail_data = 1, "Rp_acc not found", RpAccGuid
				if not DivId:
					fail_code, fail_message, fail_data = 1, "Division not found", DivGuid
				if not WhId:
					fail_code, fail_message, fail_data = 1, "Warehouse not found", WhGuid

				print(f"{RpAccId}, {DivId}, {WhId}")
				raise Exception

			if thisInv:
				invoice_data['InvId'] = thisInv.InvId
				thisInv.update(**invoice_data)
				db.session.commit()

			else:
				thisInv = Invoice(**invoice_data)
				db.session.add(thisInv)
				db.session.commit()

			inv_lines, failed_inv_lines = [], []

			for inv_line_req in inv_req['Inv_lines']:
				line_fail_code, line_fail_message, line_fail_data = 1, "", None
				inv_line_data = add_Inv_line_dict(inv_line_req)
				inv_line_data['InvId'] = thisInv.InvId
				try:
					inv_line_data['CurrencyId'] = [currency.CurrencyId for currency in db_Currencies if currency.CurrencyCode == inv_line_req["CurrencyCode"]][0]
				except:
					print("Currency not found in inv line request")
					line_fail_code, line_fail_message, line_fail_data = 1, "Currency not found", inv_line_req["CurrencyCode"]

				this_line_resource = Resource.query\
					.filter_by(
						ResRegNo = inv_line_req['ResRegNo'],
						ResGuid = inv_line_req['ResGuid'],
						GCRecord = None)\
					.first()
				
				if not this_line_resource:
					line_fail_code, line_fail_message, line_fail_data = 1, "Resource not found", inv_line_req['ResGuid']
					print(f'Inv_line api exception: Resource not found {inv_line_req["ResGuid"]}')
					raise Exception

				try:
					inv_line_data["ResId"] = this_line_resource.ResId					
					thisInvLine = Inv_line.query\
						.filter_by(
							#InvLineRegNo = inv_line_data['InvLineRegNo'],
							InvLineGuid = inv_line_data['InvLineGuid'],
							GCRecord = None)\
						.first()

					if thisInvLine:
						inv_line_data["InvLineId"] = thisInvLine.InvLineId
						thisInvLine.update(**inv_line_data)

					else:
						thisInvLine = Invoice(**inv_line_data)
						db.session.add(thisInvLine)
					
					db.session.commit()
					inv_lines.append(inv_line_req)
					thisInvLine = None

				except Exception as ex:
					print(f"{datetime.now()} | Inv Api OInvLine Exception: {ex}")
					inv_line_req["fail_code"] = line_fail_code
					inv_line_req["fail_message"] = line_fail_message
					inv_line_req["fail_data"] = line_fail_data
					failed_inv_lines.append(inv_line_req)

			invoice_data['Inv_lines'] = inv_lines
			data.append(invoice_data)

			#if whInv:
			#	add_wh_invoice(invoice)

		except Exception as ex:
			print(f"{datetime.now()} | Inv Api Exception: {ex}")
			invoice_data["fail_code"] = fail_code
			invoice_data["fail_message"] = fail_message
			invoice_data["fail_data"] = fail_data
			fails.append(invoice_data)

	return data, fails