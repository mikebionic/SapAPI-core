# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from main_pack.models import (
	Rp_acc,
	Order_inv,
	User,
)

from main_pack import db
from main_pack.config import Config

from .add_Order_inv_dict import add_Order_inv_dict
from .save_order_line_checkout_data import save_order_line_checkout_data

from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.base.num2text import price2text
from main_pack.api.common import (
	fetch_and_generate_RegNo,
	get_last_Work_period,
	get_last_Warehouse_by_DivId,
	get_ResPriceGroupId,
	get_payment_method_by_id,
	get_currency_model_from_code,
)


def save_order_checkout_data(req, model_type, current_user, session = None):
	req["orderInv"]["OInvGuid"] = str(uuid.uuid4())
	try:
		order_invoice_info = add_Order_inv_dict(req["orderInv"])
		
		orderRegNo = None
		if "OInvRegNo" in req["orderInv"]:
			orderRegNo = req["orderInv"]["OInvRegNo"] if req["orderInv"]["OInvRegNo"] else None

		InvStatId = None
		if "InvStatId" in req["orderInv"]:
			InvStatId = int(req["orderInv"]["InvStatId"]) if req["orderInv"]["InvStatId"] else None

		PmId = req["orderInv"]["PmId"]
		if not PmId:
			raise Exception

		payment_method = get_payment_method_by_id(PmId)
		if not payment_method:
			raise Exception

		if not req["orderInv"]["OrderInvLines"]:
			raise Exception
		order_inv_lines_req = req["orderInv"]["OrderInvLines"]

		if model_type == "rp_acc":
			user_id = current_user.user.UId
			user_short_name = current_user.user.UShortName
			RpAccId = current_user.RpAccId

		if model_type == "device":
			current_user = current_user.user
			model_type = "user"

		if model_type == "user":
			user_id = current_user.UId
			user_short_name = current_user.UShortName

			RpAccGuid = req["orderInv"]["RpAccGuid"]
			rp_acc = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
			RpAccId = rp_acc.RpAccId if rp_acc else None
			if not RpAccId:
				print("v1 checkout | no such rp acc")
				raise Exception
		
		if not user_id:
			main_first_user = User.query\
				.filter_by(GCRecord = None, UTypeId = 1)\
				.first()
			user_id = main_first_user.UId
			user_short_name = main_first_user.UShortName

		DivId = current_user.DivId
		CId = current_user.CId

		RegNo, pred_reg_num = fetch_and_generate_RegNo(
			user_id,
			user_short_name,
			'sale_order_invoice_code',
			orderRegNo
		)
		if not RegNo:
			print("no reg no")
			raise Exception

		work_period = get_last_Work_period()
		if not work_period:
			print("no work period")
			raise Exception

		warehouse = get_last_Warehouse_by_DivId(DivId)
		if not warehouse:
			print("no warehous")
			raise Exception
		WhId = warehouse.WhId

		order_invoice_info["OInvRegNo"] = RegNo
		order_invoice_info["InvStatId"] = InvStatId if InvStatId == 13 else 1
		order_invoice_info["OInvTypeId"] = 2
		order_invoice_info["WpId"] = work_period.WpId
		order_invoice_info["WhId"] = WhId
		order_invoice_info["DivId"] = DivId
		order_invoice_info["CId"] = CId
		order_invoice_info["RpAccId"] = RpAccId
		order_invoice_info["UId"] = user_id

		currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE
		if "CurrencyCode" in req["orderInv"]:
			currency_code = req["orderInv"]["CurrencyCode"] if req["orderInv"]["CurrencyCode"] else currency_code

		inv_currency = get_currency_model_from_code(
			currency_code = currency_code,
			session = session,
		)
		if not inv_currency:
			print(f"{datetime.now()} | v1 Order Checkout exception: No currency found")
			raise Exception

		order_invoice_info["CurrencyId"] = inv_currency.CurrencyId

		this_Order_inv = Order_inv(**order_invoice_info)
		db.session.add(this_Order_inv)
		db.session.commit()

		ResPriceGroupId = get_ResPriceGroupId(model_type, current_user, session)

		data, fails, OInvTotal = save_order_line_checkout_data(
			req = order_inv_lines_req,
			OInvId = this_Order_inv.OInvId,
			user_id = user_id,
			user_short_name = user_short_name,
			WhId = WhId,
			ResPriceGroupId = ResPriceGroupId,
			check_price_value = 1 if model_type != "user" else 0,
			inv_currency = inv_currency,
		)

		if fails:
			res = {
				"data": order_invoice_info,
				"successes": data,
				"fails": fails,
				"success_total": len(data),
				"fail_total": len(fails),
				"total": len(order_inv_lines_req)
			}

			db.session.delete(this_Order_inv)
			db.session.commit()

		else:
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(
				OInvFTotal,
				Config.PRICE_2_TEXT_LANGUAGE,
				inv_currency.CurrencyCode,
			)

			this_Order_inv.OInvTotal = round(float(OInvTotal), 2)
			this_Order_inv.OInvFTotal = round(float(OInvFTotal), 2)
			this_Order_inv.OInvFTotalInWrite = OInvFTotalInWrite

			if pred_reg_num and InvStatId == 1:
				db.session.delete(pred_reg_num)

			db.session.commit()

			res = {
				"data": this_Order_inv.to_json_api(),
				"successes": data,
				"fails": fails,
				"success_total": len(data),
				"fail_total": len(fails) or 0,
				"total": len(order_inv_lines_req)
			}

		status = checkApiResponseStatus(data, fails)
		for e in status:
			res[e] = status[e]

	except Exception as ex:
		print(f"{datetime.now()} | Checkout OInv Exception: {ex}")
		res = {
			"data": order_invoice_info,
			"message": "Failed to checkout order",
			"status": 0,
		}

	return res