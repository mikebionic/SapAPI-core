
from main_pack.config import Config
from main_pack.models import Currency

def get_currency_from_code(
	currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE,
	session = None,
	Currency_dbModel = None,
):

	if not Currency_dbModel:
		Currency_dbModel = Currency.query.filter_by(GCRecord = None).all()

	if session:
		if "currency_code" in session:
			currency_code = session["currency_code"] if session["currency_code"] else currency_code

	currency = [currency for currency in Currency_dbModel if currency.CurrencyCode == currency_code]
	currency = currency[0] if currency else None

	return currency