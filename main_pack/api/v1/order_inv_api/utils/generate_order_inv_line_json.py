# -*- coding: utf-8 -*-
from main_pack.base.priceMethods import price_currency_conversion
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def generate_order_inv_line_json(
	order_inv,
	currencies,
	exc_rates,
	show_inv_line_resource,
	currency_code = None,
):
	order_inv_lines = []
	for order_inv_line in order_inv.Order_inv_line:
		if not order_inv_line.GCRecord:
			this_order_inv_line = order_inv_line.to_json_api()
			this_order_inv_line["ResRegNo"] = order_inv_line.resource.ResRegNo if order_inv_line.resource and not order_inv_line.resource.GCRecord else None
			this_order_inv_line["ResGuid"] = order_inv_line.resource.ResGuid if order_inv_line.resource and not order_inv_line.resource.GCRecord else None

			currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == order_inv_line.CurrencyId]

			if not currency_data:
				print("order_inv_api line exception: no currency specified")
				raise Exception

			this_line_Price = this_order_inv_line["OInvLinePrice"]
			this_line_Total = this_order_inv_line["OInvLineTotal"]
			this_line_FTotal = this_order_inv_line["OInvLineFTotal"]
			this_line_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None
			ExcRateValue = this_order_inv_line["ExcRateValue"]

			# print(f"requested code: {currency_code} of line with code {this_line_currencyCode} | Inv rate is {ExcRateValue}")
			price_conversion_args = {
				"from_currency": this_line_currencyCode,
				"to_currency": currency_code if currency_code else this_line_currencyCode,
				"currencies_dbModel": currencies,
				"exc_rates_dbModel": exc_rates,
				"from_exc_rate_value": ExcRateValue,
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
			# print(f"converted from {this_line_Price} to {price_data['ResPriceValue']} with rate {price_data['ExcRateValue']}")
			this_order_inv_line["OInvLinePrice"] = price_data["ResPriceValue"]
			this_order_inv_line["CurrencyId"] = price_data["CurrencyId"]
			this_order_inv_line["CurrencyCode"] = price_data["CurrencyCode"]
			this_order_inv_line["ExcRateValue"] = price_data["ExcRateValue"]
			this_order_inv_line["OInvLineTotal"] = Total_price_data["ResPriceValue"]
			this_order_inv_line["OInvLineFTotal"] = FTotal_price_data["ResPriceValue"]


			if show_inv_line_resource:
				resource_json = apiResourceInfo(
					resource_list = [{"ResId": order_inv_line.ResId}],
					avoidQtyCheckup = 1,
					single_object = True)
				this_order_inv_line["Resource"] = resource_json["data"]

			order_inv_lines.append(this_order_inv_line)

	return order_inv_lines