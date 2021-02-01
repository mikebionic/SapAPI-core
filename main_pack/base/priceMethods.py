from datetime import datetime

from main_pack import Config
from main_pack.models.commerce.models import Exc_rate

main_currency = "USD"
from_currency = "USD"
to_currency = "TMT"
def price_currency_conversion(
	main_currency = None,
	from_currency = None,
	to_currency = None,
	currencies_dbModel = None,
	exc_rates_dbModel = None):
	if not currencies_dbModel:
		currencies_dbModel = Currency.query.all()

	if not exc_rates_dbModel:
		exc_rates_dbModel = Exc_rate.query.filter_by(GCRecord = None).all()

	if not from_currency:
		from_currency = Config.MAIN_CURRENCY_CODE

	if not to_currency:
		to_currency = Config.DEFAULT_VIEW_CURRENCY_CODE

	main_currency_data = [currency for currency in currencies_dbModel if currency.CurrencyCode == main_currency]
	from_currency_data = [currency for currency in currencies_dbModel if currency.CurrencyCode == from_currency]
	to_currency_data = [currency for currency in currencies_dbModel if currency.CurrencyCode == to_currency]

	from_exchange_rate = [for exc_rate in exc_rates_dbModel if exc_rate.CurrencyId == from_currency_data.CurrencyId and not exc_rate.GCRecord]
	to_exchange_rate = [for exc_rate in exc_rates_dbModel if exc_rate.CurrencyId == to_currency_data.CurrencyId and not exc_rate.GCRecord]


def calculatePriceByGroup(ResPriceGroupId, Res_price_dbModels, Res_pice_group_dbModels):
	data = []
	try:
		if not ResPriceGroupId:
			data = [res_price.to_json_api() 
				for res_price in Res_price_dbModels
				if res_price.ResPriceTypeId == 2
				and not res_price.GCRecord]

		if ResPriceGroupId:
			data = [res_price.to_json_api() 
				for res_price in Res_price_dbModels 
				if res_price.ResPriceTypeId == 2 
				and res_price.ResPriceGroupId == ResPriceGroupId
				and not res_price.GCRecord]

			if not data:
				thisPriceGroupList = [priceGroup for priceGroup in Res_pice_group_dbModels if priceGroup.ResPriceGroupId == ResPriceGroupId]
				if thisPriceGroupList:
					if not thisPriceGroupList[0].ResPriceGroupAMEnabled:
						raise Exception

					FromResPriceTypeId = thisPriceGroupList[0].FromResPriceTypeId
					ResPriceGroupAMPerc = thisPriceGroupList[0].ResPriceGroupAMPerc

					data = [res_price.to_json_api() 
						for res_price in Res_price_dbModels 
						if res_price.ResPriceTypeId == FromResPriceTypeId
						and not res_price.GCRecord]

					if not data:
						raise Exception

					CalculatedPriceValue = float(data[0]["ResPriceValue"]) + (float(data[0]["ResPriceValue"]) * float(ResPriceGroupAMPerc) / 100)
					data[0]["ResPriceValue"] = CalculatedPriceValue

	except Exception as ex:
		# print(f"{datetime.now()} | Res price calculation Exception: {ex}")
		pass

	return data