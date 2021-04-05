# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack.models import Currency
from main_pack.models import Exc_rate
from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.priceMethods import price_currency_conversion
from .generate_invoice_line_json import generate_invoice_line_json

def generate_invoice_json(
	rp_acc_user,
	invoices_only,
	invoice_models,
	currency_code,
	show_inv_line_resource
):

	currencies = Currency.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	data, fails = [], []
	for invoice_object in invoice_models:
		try:
			invoice_object_info = invoice_object.to_json_api()

			inv_status = invoice_object.inv_status.to_json_api() if invoice_object.inv_status and not invoice_object.inv_status.GCRecord else None
			inv_status = dataLangSelector(inv_status)
			invoice_object_info["InvStatName"] = inv_status["InvStatName"]

			currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == invoice_object.CurrencyId]

			if not currency_data:
				print("invoice_api exception: no currency specified")
				raise Exception

			this_Total = invoice_object_info["InvTotal"]
			this_FTotal = invoice_object_info["InvFTotal"]
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

			invoice_object_info["InvTotal"] = price_data["ResPriceValue"]
			invoice_object_info["InvFTotal"] = FTotal_price_data["ResPriceValue"]
			invoice_object_info["CurrencyId"] = price_data["CurrencyId"]
			invoice_object_info["CurrencyCode"] = price_data["CurrencyCode"]

			rp_acc_data = {}
			if rp_acc_user:
				rp_acc_data = rp_acc_user.to_json_api()

			elif invoice_object.rp_acc:
				rp_acc_data = invoice_object.rp_acc.to_json_api()

			invoice_object_info["Rp_acc"] = rp_acc_data
			invoice_object_info["CGuid"] = invoice_object.company.CGuid if invoice_object.company and not invoice_object.company.GCRecord else None
			invoice_object_info["WhGuid"] = invoice_object.warehouse.WhGuid if invoice_object.warehouse and not invoice_object.warehouse.GCRecord else None
			invoice_object_info["DivGuid"] = invoice_object.division.DivGuid if invoice_object.division and not invoice_object.division.GCRecord else None
			invoice_object_info["RpAccGuid"] = invoice_object.rp_acc.RpAccGuid if invoice_object.rp_acc and not invoice_object.rp_acc.GCRecord else None
			invoice_object_info["RpAccRegNo"] = invoice_object.rp_acc.RpAccRegNo if invoice_object.rp_acc and not invoice_object.rp_acc.GCRecord else None

			# !!! Check the send and get type of these params (root or structured?)
			rp_acc_user = None

			if not invoices_only:
				invoice_object_info["Inv_lines"] = generate_invoice_line_json(
					invoice_object,
					currencies,
					exc_rates,
					currency_code,
					show_inv_line_resource,
				)

			data.append(invoice_object_info)

		except Exception as ex:
			print(f"{datetime.now()} | Invoice info utils Exception: {ex}")
			fails.append(invoice_object.to_json_api())

	return data, fails