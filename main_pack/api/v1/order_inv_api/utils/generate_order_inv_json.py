# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack.models.base.models import Currency
from main_pack.models.commerce.models import Exc_rate
from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.priceMethods import price_currency_conversion
from .generate_order_inv_line_json import generate_order_inv_line_json

def generate_order_inv_json(
	rp_acc_user,
	invoices_only,
	invoice_models,
	currency_code,
	show_inv_line_resource
):

	currencies = Currency.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	data, fails = [], []
	for order_inv in invoice_models:
		try:
			order_inv_info = order_inv.to_json_api()

			inv_status = order_inv.inv_status.to_json_api() if order_inv.inv_status and not order_inv.inv_status.GCRecord else None
			inv_status = dataLangSelector(inv_status)
			order_inv_info["InvStatName"] = inv_status["InvStatName"]

			currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == order_inv.CurrencyId]

			if not currency_data:
				print("order_inv_api exception: no currency specified")
				raise Exception

			this_Total = order_inv_info["OInvTotal"]
			this_FTotal = order_inv_info["OInvFTotal"]
			this_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None

			price_conversion_args = {
				"from_currency": this_currencyCode,
				"to_currency": currency_code,
				"currencies_dbModel": currencies,
				"exc_rates_dbModel": exc_rates
			}

			price_data = price_currency_conversion(
				priceValue = this_Total,
				**price_conversion_args
			)

			FTotal_price_data = price_currency_conversion(
				priceValue = this_FTotal,
				**price_conversion_args
			)

			order_inv_info["OInvTotal"] = price_data["ResPriceValue"]
			order_inv_info["OInvFTotal"] = FTotal_price_data["ResPriceValue"]
			order_inv_info["CurrencyId"] = price_data["CurrencyId"]
			order_inv_info["CurrencyCode"] = price_data["CurrencyCode"]

			rp_acc_data = {}
			if rp_acc_user:
				rp_acc_data = rp_acc_user.to_json_api()

			elif order_inv.rp_acc:
				rp_acc_data = order_inv.rp_acc.to_json_api()

			# !!! Deprecated
			rp_acc_data["Images"] = []

			order_inv_info["Rp_acc"] = rp_acc_data
			order_inv_info["CGuid"] = order_inv.company.CGuid if order_inv.company and not order_inv.company.GCRecord else None
			order_inv_info["WhGuid"] = order_inv.warehouse.WhGuid if order_inv.warehouse and not order_inv.warehouse.GCRecord else None
			order_inv_info["DivGuid"] = order_inv.division.DivGuid if order_inv.division and not order_inv.division.GCRecord else None
			order_inv_info["RpAccGuid"] = order_inv.rp_acc.RpAccGuid if order_inv.rp_acc and not order_inv.rp_acc.GCRecord else None
			order_inv_info["RpAccRegNo"] = order_inv.rp_acc.RpAccRegNo if order_inv.rp_acc and not order_inv.rp_acc.GCRecord else None

			rp_acc_user = None

			if not invoices_only:
				order_inv_info["Order_inv_lines"] = generate_order_inv_line_json(
					order_inv,
					currencies,
					exc_rates,
					currency_code,
					show_inv_line_resource,
				)

			data.append(order_inv_info)

		except Exception as ex:
			print(f"{datetime.now()} | Order_inv info utils Exception: {ex}")
			fails.append(order_inv.to_json_api())

	return data, fails