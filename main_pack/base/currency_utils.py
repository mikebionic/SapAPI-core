from main_pack import Config

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

	if not to_currency:
		to_currency = Config.DEFAULT_VIEW_CURRENCY_CODE if Config.Default

	main_currency_data = [currency.to_json_api() for currency in currencies_dbModel if currency.CurrencyCode == main_currency]
	from_currency_data = [currency.to_json_api() for currency in currencies_dbModel if currency.CurrencyCode == from_currency]
	to_currency_data = [currency.to_json_api() for currency in currencies_dbModel if currency.CurrencyCode == to_currency]