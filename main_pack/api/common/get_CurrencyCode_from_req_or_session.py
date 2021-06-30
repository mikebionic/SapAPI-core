from main_pack.config import Config

def get_CurrencyCode_from_req_or_session(payload, session):
	currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE
	if "CurrencyCode" in payload:
		currency_code = payload["CurrencyCode"] if payload["CurrencyCode"] else currency_code
	elif "currency_code" in session:
		currency_code = session["currency_code"] if session["currency_code"] else currency_code
	currency_code = currency_code.upper()

	return currency_code