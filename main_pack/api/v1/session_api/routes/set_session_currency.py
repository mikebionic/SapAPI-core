from flask import (
	jsonify,
	session,
)

from main_pack.models import Currency
from main_pack.api.v1.session_api import api

@api.route('/set-session-currency/<currency_code>/')
def set_session_currency(currency_code):
	currency = Currency.query.filter_by(CurrencyCode = currency_code).first()
	if currency_code:
		session['currency_code'] = currency.CurrencyCode
		status_code = 200

	else:
		session['currency_code'] = Config.DEFAULT_VIEW_CURRENCY_CODE
		status_code = 404

	res = {
		"status": 1 if currency else 0,
		"data": session['currency_code'],
		"message": "Session CurrencyCode",
	}
	return jsonify(res), status_code