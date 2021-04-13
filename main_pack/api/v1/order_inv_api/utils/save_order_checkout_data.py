# -*- coding: utf-8 -*-

import uuid

from main_pack import 
from main_pack.models import (
	Rp_acc,
	Order_inv,
	Order_inv_line,
)

from .add_Order_inv_dict import add_Order_inv_dict
from .add_Order_inv_line_dict import add_Order_inv_line_dict
from main_pack.api.common import (
	fetch_and_generate_RegNo,
	get_last_Work_period,
	get_last_Warehouse_by_DivId,
)


def save_order_checkout_data(req, model_type, current_user):
	req['orderInv']['OInvGuid'] = str(uuid.uuid4())
	try:
		order_invoice_info = add_Order_inv_dict(req['orderInv'])
		orderRegNo = req['orderInv']['OInvRegNo']
		InvStatId = int(req['orderInv']['InvStatId'])

		if not req['orderInv']['OrderInvLines']:
			raise Exception

		if model_type == "user":
			user_id = current_user.UId
			user_short_name = current_user.UShortName
			RpAccGuid = req['RpAccGuid']

			rp_acc = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
			RpAccId = rp_acc.RpAccId if rp_acc else None
			if not RpAccId:
				raise Exception

		elif model_type == "rp_acc":
			user_id = current_user.user.UId
			user_short_name = current_user.user.UShortName
			RpAccId = current_user.RpAccId

		DivId = current_user.DivId
		CId = current_user.CId
		
		RegNo = fetch_and_generate_RegNo(
			user_id,
			user_short_name,
			'sale_order_invoice_code',
			orderRegNo
		)
		if not RegNo:
			raise Exception

		work_period = get_last_Work_period()
		if not work_period:
			raise Exception

		warehouse = get_last_Warehouse_by_DivId(DivId)
		if not warehouse:
			raise Exception


		order_invoice_info["OInvRegNo"] = RegNo
		order_invoice_info["InvStatId"] = 1
		order_invoice_info["OInvTypeId"] = 2
		order_invoice_info["WpId"] = work_period.WpId
		order_invoice_info["WhId"] = warehouse.WhId
		order_invoice_info["DivId"] = DivId
		order_invoice_info["CId"] = CId
		if InvStatId == 13:
			order_invoice_info["InvStatId"] = InvStatId

		if not order_invoice_info["CurrencyId"]:
			order_invoice_info["CurrencyId"] = 1
		order_invoice_info["RpAccId"] = RpAccId

		this_Order_inv = Order_inv(**order_invoice_info)
		db.session.add(this_Order_inv)

		data, fails = [], []
		OInvTotal = 0
		OrderInvLines = req['orderInv']['OrderInvLines']
		for order_inv_line_req in OrderInvLines:
			try:
				# in case of errors, the error_type is provided
				error_type = 0
				order_inv_line_req['OInvLineGuid'] = str(uuid.uuid4())
				order_inv_line = addOrderInvLineDict(order_inv_line_req)
				# OInvLineRegNo generation
				try:
					reg_num = generate(UId=user.UId,RegNumTypeName='order_invoice_line_code')
					orderLineRegNo = makeRegNo(user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'',True)
				except Exception as ex:
					print(f"{datetime.now()} | Checkout OInv Exception: {ex}. Couldn't generate RegNo using User's credentials")
					# use device model and other info
					orderLineRegNo = str(datetime.now().replace(tzinfo=timezone.utc).timestamp())
				order_inv_line["OInvLineRegNo"] = orderLineRegNo
				orderLineRegNo = None

				ResId = order_inv_line["ResId"]
				OInvLineAmount = int(order_inv_line["OInvLineAmount"])

				resource = Resource.query\
					.filter_by(GCRecord = None, ResId = ResId)\
					.options(joinedload(Resource.Res_price))\
					.first()

				if not resource:
					# type deleted or none
					error_type = 1
					raise Exception

				List_Res_price = calculatePriceByGroup(
					ResPriceGroupId = ResPriceGroupId,
					Res_price_dbModels = resource.Res_price,
					Res_pice_group_dbModels = res_price_groups)

				if not List_Res_price:
					raise Exception

				try:
					List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == List_Res_price[0]["CurrencyId"]]
				except:
					List_Currencies = []

				this_priceValue = List_Res_price[0]["ResPriceValue"] if List_Res_price else 0.0
				this_currencyCode = List_Currencies[0]["CurrencyCode"] if List_Currencies else Config.MAIN_CURRENCY_CODE

				price_data = price_currency_conversion(
					priceValue = this_priceValue,
					from_currency = this_currencyCode,
					currencies_dbModel = currencies,
					exc_rates_dbModel = exc_rates)

				res_total = Res_total.query\
					.filter_by(GCRecord = None, ResId = ResId, WhId = WhId)\
					.first()
				totalSubstitutionResult = totalQtySubstitution(res_total.ResPendingTotalAmount,OInvLineAmount)

				if resource.UsageStatusId == 2:
					# resource unavailable or inactive
					error_type = 2
					raise Exception

				if totalSubstitutionResult["status"] == 0:
					# resource is empty or bad request with amount = -1
					error_type = 3
					raise Exception

				if order_inv_line["OInvLinePrice"] != price_data["ResPriceValue"]:
					error_type = 4
					raise Exception

				OInvLineAmount = totalSubstitutionResult["amount"]
				# ResPendingTotalAmount is decreased but not ResTotBalance
				res_total.ResPendingTotalAmount = totalSubstitutionResult["totalBalance"]
				############
				OInvLinePrice = float(price_data["ResPriceValue"])
				OInvLineTotal = OInvLinePrice * OInvLineAmount

				# add taxes and stuff later on
				OInvLineFTotal = OInvLineTotal

				###### inv line assignment ######
				order_inv_line["OInvLineAmount"] = decimal.Decimal(OInvLineAmount)
				order_inv_line["OInvLinePrice"] = decimal.Decimal(OInvLinePrice)
				order_inv_line["OInvLineTotal"] = decimal.Decimal(OInvLineTotal)
				order_inv_line["OInvLineFTotal"] = decimal.Decimal(OInvLineFTotal)
				order_inv_line["OInvId"] = this_Order_inv.OInvId
				order_inv_line["UnitId"] = resource.UnitId
				order_inv_line["CurrencyId"] = price_data["CurrencyId"]

				# increment of Main Order Inv Total Price
				OInvTotal += OInvLineFTotal
				thisOInvLine = Order_inv_line(**order_inv_line)
				db.session.add(thisOInvLine)
				data.append(thisOInvLine.to_json_api())

				order_inv_line = None

			except Exception as ex:
				print(f"{datetime.now()} | Checkout OInv Line Exception: {ex} | Error type {error_type}")
				fail_info = {
					"data": order_inv_line_req,
					"error_type_id": error_type,
					"error_type_message": get_order_error_type(error_type)
				}
				fails.append(fail_info)

		###### final order assignment and processing ######
		# add taxes and stuff later on
		if fails:
			status = checkApiResponseStatus(data,fails)
			res = {
				"data": order_invoice_info,
				"successes": data,
				"fails": fails,
				"success_total": len(data),
				"fail_total": len(fails),
				"total": len(OrderInvLines)
			}
			status_code = 400
			for e in status:
				res[e] = status[e]

		else:
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(
				OInvFTotal,
				Config.PRICE_2_TEXT_LANGUAGE,
				price_data["CurrencyCode"])

			this_Order_inv.OInvTotal = decimal.Decimal(OInvTotal)
			this_Order_inv.OInvFTotal = decimal.Decimal(OInvFTotal)
			this_Order_inv.OInvFTotalInWrite = OInvFTotalInWrite

			if reg_num_pred_exists:
				db.session.delete(reg_num_pred_exists)

			db.session.commit()

			status = checkApiResponseStatus(data, fails)

			res = {
				"data": this_Order_inv.to_json_api(),
				"successes": data,
				"fails": fails,
				"success_total": len(data),
				"fail_total": len(fails) or 0,
				"total": len(OrderInvLines)
			}

			# status_code = 201 if len(order_invoice_info) > 0 else 200
			status_code = 200
			for e in status:
				res[e] = status[e]

	except Exception as ex:
		print(f"{datetime.now()} | Checkout OInv Exception: {ex}")
		res = {
			"data": order_invoice_info,
			"message": "Failed to checkout order"
		}
		status_code = 400