# -*- coding: utf-8 -*-
from main_pack.base.priceMethods import price_currency_conversion
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def generate_invoice_line_json(
	invoice_object,
	currencies,
	exc_rates,
	currency_code,
	show_inv_line_resource,
):
	invoice_object_lines = []
	for invoice_object_line in invoice_object.Inv_line:
		if not invoice_object_line.GCRecord:
			this_invoice_object_line = invoice_object_line.to_json_api()
			this_invoice_object_line["ResRegNo"] = invoice_object_line.resource.ResRegNo if invoice_object_line.resource and not invoice_object_line.resource.GCRecord else None
			this_invoice_object_line["ResGuid"] = invoice_object_line.resource.ResGuid if invoice_object_line.resource and not invoice_object_line.resource.GCRecord else None

			currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == invoice_object_line.CurrencyId]

			if not currency_data:
				print("order_inv_api line exception: no currency specified")
				raise Exception

			this_line_Price = this_invoice_object_line["InvLinePrice"]
			this_line_Total = this_invoice_object_line["InvLineTotal"]
			this_line_FTotal = this_invoice_object_line["InvLineFTotal"]
			this_line_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None
			ExcRateValue = this_invoice_object_line["ExcRateValue"]

			price_conversion_args = {
				"from_currency": this_line_currencyCode,
				"to_currency": currency_code,
				"currencies_dbModel": currencies,
				"exc_rates_dbModel": exc_rates,
				"exc_rate_value": ExcRateValue,
			}

			price_data = price_currency_conversion(
				priceValue = this_line_Price,
				**price_conversion_args
			)

			Total_price_data = price_currency_conversion(
				priceValue = this_line_Total,
				**price_conversion_args
			)

			FTotal_price_data = price_currency_conversion(
				priceValue = this_line_FTotal,
				**price_conversion_args
			)

			this_invoice_object_line["InvLinePrice"] = price_data["ResPriceValue"]
			this_invoice_object_line["CurrencyId"] = price_data["CurrencyId"]
			this_invoice_object_line["CurrencyCode"] = price_data["CurrencyCode"]
			this_invoice_object_line["InvLineTotal"] = Total_price_data["ResPriceValue"]
			this_invoice_object_line["InvLineFTotal"] = FTotal_price_data["ResPriceValue"]


			if show_inv_line_resource:
				resource_json = apiResourceInfo(
					resource_list = [{"ResId": invoice_object_line.ResId}],
					avoidQtyCheckup = 1,
					single_object = True)
				this_invoice_object_line["Resource"] = resource_json["data"]

			invoice_object_lines.append(this_invoice_object_line)
