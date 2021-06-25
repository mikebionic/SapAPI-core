# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from sqlalchemy.orm import joinedload

from main_pack.models import (
	Order_inv_line,
	Resource,
	Res_total,
	Currency,
	Res_price_group,
	Exc_rate,
)

from main_pack import db
from main_pack.config import Config
from main_pack.base.invoiceMethods import totalQtySubstitution, get_order_error_type
from main_pack.base.priceMethods import calculatePriceByGroup, price_currency_conversion
from main_pack.api.common import (
	fetch_and_generate_RegNo,
)

from .add_Order_inv_line_dict import add_Order_inv_line_dict


def save_order_line_checkout_data(
	req,
	OInvId,
	user_id,
	user_short_name,
	WhId = None,
	ResPriceGroupId = None,
	check_price_value = 1,
	inv_currency = None,
):

	currencies = Currency.query.filter_by(GCRecord = None).all()
	res_price_groups = Res_price_group.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	data, fails, data_models = [], [], []
	OInvTotal = 0
	for order_inv_line_req in req:
		try:
			error_type = 0
			order_inv_line_req['OInvLineGuid'] = str(uuid.uuid4())
			order_inv_line = add_Order_inv_line_dict(order_inv_line_req)

			RegNo, _ = fetch_and_generate_RegNo(
				user_id,
				user_short_name,
				'order_invoice_line_code',
			)
			if not RegNo:
				raise Exception

			order_inv_line["OInvLineRegNo"] = RegNo
			print(RegNo)
			RegNo = None

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

			if resource.UsageStatusId == 2:
				# resource unavailable or inactive
				error_type = 2
				raise Exception

			res_total = Res_total.query\
				.filter_by(GCRecord = None, ResId = ResId, WhId = WhId)\
				.first()
			totalSubstitutionResult = totalQtySubstitution(res_total.ResPendingTotalAmount,OInvLineAmount)
			OInvLineAmount = totalSubstitutionResult["amount"]
			res_total.ResPendingTotalAmount = totalSubstitutionResult["totalBalance"]

			if totalSubstitutionResult["status"] == 0:
				# resource is empty or bad request with amount = -1
				error_type = 3
				raise Exception

			List_Res_price = calculatePriceByGroup(
				ResPriceGroupId = ResPriceGroupId,
				Res_price_dbModels = resource.Res_price,
				Res_pice_group_dbModels = res_price_groups
			)
			if not List_Res_price:
				raise Exception

			# print(List_Res_price)
			# print("------------")
			# print(resource.Res_price[0].to_json_api())
			# print("------------")

			this_Resource_PriceValue = List_Res_price[0]["ResPriceValue"] if List_Res_price[0]["ResPriceValue"] else 0.0
			List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == List_Res_price[0]["CurrencyId"]]

			if not List_Currencies:
				List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyCode == Config.MAIN_CURRENCY_CODE]
				# print("Save Order Line checkout | Currency not found or empty")
				# raise Exception

			this_Resource_CurrencyCode = List_Currencies[0]["CurrencyCode"]
			this_Resource_CurrencyId = List_Currencies[0]["CurrencyId"]

			this_currencyCode = inv_currency.CurrencyCode
			this_currencyId = inv_currency.CurrencyId

			Resource_price_data = price_currency_conversion(
				priceValue = this_Resource_PriceValue,
				from_currency = this_Resource_CurrencyCode,
				to_currency = this_currencyCode,
				currencies_dbModel = currencies,
				exc_rates_dbModel = exc_rates)

			PriceValue = float(Resource_price_data["ResPriceValue"]) if check_price_value else float(order_inv_line["OInvLinePrice"])
			CurrencyId = Resource_price_data["CurrencyId"]
			CurrencyCode = Resource_price_data["CurrencyCode"]
			ExcRateValue = Resource_price_data["ExcRateValue"]

			# print("--------------------------")
			# print(Resource_price_data)
			# print(order_inv_line["OInvLinePrice"])
			# print("--------------------------")
			if order_inv_line["OInvLinePrice"] != PriceValue:
				print(f"{PriceValue} given,order inv line is {order_inv_line['OInvLinePrice']}")
				error_type = 4
				raise Exception

			OInvLinePrice = PriceValue
			OInvLineTotal = OInvLinePrice * OInvLineAmount
			# add taxes and stuff later on
			OInvLineFTotal = OInvLineTotal

			order_inv_line["OInvLineAmount"] = round(float(OInvLineAmount), 2)
			order_inv_line["OInvLinePrice"] = round(float(OInvLinePrice), 2)
			order_inv_line["OInvLineTotal"] = round(float(OInvLineTotal), 2)
			order_inv_line["OInvLineFTotal"] = round(float(OInvLineFTotal), 2)
			order_inv_line["OInvId"] = OInvId
			order_inv_line["UnitId"] = resource.UnitId
			order_inv_line["CurrencyId"] = CurrencyId
			order_inv_line["ExcRateValue"] = ExcRateValue

			OInvTotal += OInvLineFTotal
			thisOInvLine = Order_inv_line(**order_inv_line)
			db.session.add(thisOInvLine)
			data.append(thisOInvLine.to_json_api())
			data_models.append(thisOInvLine)

			order_inv_line = None

		except Exception as ex:
			print(f"{datetime.now()} | Checkout OInv Line Exception: {ex} | Error type {error_type}")
			fail_info = {
				"data": order_inv_line_req,
				"error_type_id": error_type,
				"error_type_message": get_order_error_type(error_type)
			}
			fails.append(fail_info)

	if fails:
		for model in data_models:
			db.session.expunge(model)

	return data, fails, OInvTotal