# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import db
from main_pack.config import Config
from main_pack.models import (
	Order_inv,
	Order_inv_line,
	Res_total,
	Resource,
	Currency,
)
from main_pack.api.common import (
	get_division_id_guid_list,
	get_warehouse_id_guid_list,
	get_rp_acc_id_guid_list,
	get_currency_model_from_code,
)
from .add_Order_inv_dict import add_Order_inv_dict
from .add_Order_inv_line_dict import add_Order_inv_line_dict
from main_pack.base import get_id_from_list_indexing


def save_order_inv_synch_data(req):

	data, fails = [], []

	currencies = Currency.query.filter_by(GCRecord = None).all()

	for order_inv_req in req:
		try:
			order_invoice = add_Order_inv_dict(order_inv_req)
			DivGuid = order_inv_req['DivGuid']
			WhGuid = order_inv_req['WhGuid']
			RpAccGuid = order_inv_req['RpAccGuid']

			OInvGuid = order_invoice['OInvGuid']
			OInvRegNo = order_invoice['OInvRegNo']

			DivId_list, DivGuid_list = get_division_id_guid_list()
			WhId_list, WhGuid_list = get_warehouse_id_guid_list()
			RpAccId_list, RpAccGuid_list = get_rp_acc_id_guid_list()

			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, DivGuid)
			WhId = get_id_from_list_indexing(WhId_list, WhGuid_list, WhGuid)
			RpAccId = get_id_from_list_indexing(RpAccId_list, RpAccGuid_list, RpAccGuid)

			if not RpAccId or not DivId or not WhId:
				print(f"{RpAccId}, {DivId}, {WhId}")
				raise Exception

			order_invoice['DivId'] = DivId
			order_invoice['WhId'] = WhId
			order_invoice['RpAccId'] = RpAccId

			currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE
			if "CurrencyCode" in req["orderInv"]:
				currency_code = req["orderInv"]["CurrencyCode"] if req["orderInv"]["CurrencyCode"] else currency_code

			inv_currency = get_currency_model_from_code(
				currency_code = currency_code,
				Currency_dbModels = currencies,
			)
			if not inv_currency:
				print(f"{datetime.now()} | v1 Order Checkout exception: No currency found")
				raise Exception

			order_invoice["CurrencyId"] = inv_currency.CurrencyId
			
			thisOrderInv = Order_inv.query\
				.filter_by(
					OInvGuid = OInvGuid,
					# OInvRegNo = OInvRegNo,
					GCRecord = None)\
				.first()
			thisInvStatus = None

			if thisOrderInv:
				order_invoice['OInvId'] = thisOrderInv.OInvId
				old_invoice_status = thisOrderInv.InvStatId
				thisOrderInv.update(**order_invoice)
				db.session.commit()
				# if status: "returned" or "cancelled" (id=9, id=5)
				# all lines should update
				# res_total.ResPendingTotalAmount
				thisInvStatus = thisOrderInv.InvStatId

			else:
				thisOrderInv = Order_inv(**order_invoice)
				db.session.add(thisOrderInv)
				db.session.commit()

			order_inv_lines, failed_order_inv_lines = [], []

			for order_inv_line_req in order_inv_req['Order_inv_lines']:
				order_inv_line = add_Order_inv_line_dict(order_inv_line_req)
				order_inv_line['OInvId'] = thisOrderInv.OInvId

				ResRegNo = order_inv_line_req['ResRegNo']
				ResGuid = order_inv_line_req['ResGuid']

				currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE
				if "CurrencyCode" in order_inv_line_req:
					currency_code = order_inv_line_req["CurrencyCode"] if order_inv_line_req["CurrencyCode"] else currency_code

				inv_line_currency = get_currency_model_from_code(
					currency_code = currency_code,
					Currency_dbModels = currencies,
				)
				if not inv_line_currency:
					print(f"{datetime.now()} | v1 Order Checkout exception: No currency found")
					raise Exception

				order_inv_line["CurrencyId"] = inv_line_currency.CurrencyId

				this_line_resource = Resource.query\
					.filter_by(
						ResRegNo = ResRegNo,
						ResGuid = ResGuid,
						GCRecord = None)\
					.first()

				try:
					order_inv_line["ResId"] = this_line_resource.ResId
					OInvLineRegNo = order_inv_line['OInvLineRegNo']
					OInvLineGuid = order_inv_line['OInvLineGuid']

					thisOrderInvLine = Order_inv_line.query\
						.filter_by(
							OInvLineGuid = OInvLineGuid,
							# OInvLineRegNo = OInvLineRegNo,
							GCRecord = None)\
						.first()

					if thisOrderInvLine:
						order_inv_line["OInvLineId"] = thisOrderInvLine.OInvLineId
						thisOrderInvLine.update(**order_inv_line)
						if thisInvStatus == 9 or thisInvStatus == 5:
							try:
								if (old_invoice_status != 5 or old_invoice_status != 9):
									order_res_total = Res_total.query\
										.filter_by(
											ResId = thisOrderInvLine.ResId,
											GCRecord = None)\
										.first()
									order_res_total.ResPendingTotalAmount += thisOrderInvLine.OInvLineAmount

							except Exception as ex:
								print(f"{datetime.now()} | OInv Api Res_total Exception: {ex}")

						db.session.commit()
						order_inv_lines.append(order_inv_line_req)

					else:
						thisOrderInvLine = Order_inv_line(**order_inv_line)
						db.session.add(thisOrderInvLine)
						db.session.commit()
						order_inv_lines.append(order_inv_line_req)
						thisOrderInvLine = None

				except Exception as ex:
					print(f"{datetime.now()} | OInv Api OInvLine Exception: {ex}")
					failed_order_inv_lines.append(order_inv_line_req)

			order_invoice['Order_inv_lines'] = order_inv_lines
			data.append(order_invoice)

		except Exception as ex:
			print(f"{datetime.now()} | OInv Api Exception: {ex}")
			fails.append(order_invoice)

	return data, fails