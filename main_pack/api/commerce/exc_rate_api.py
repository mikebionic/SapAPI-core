# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy.orm import joinedload

from main_pack import db
from . import api
from .utils import addExcRateDict
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json
from main_pack.api.auth.utils import sha_required

from main_pack.models.commerce.models import Exc_rate
from main_pack.models.base.models import Currency


@api.route("/tbl-dk-exc-rates/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_exc_rate():
	if request.method == 'GET':
		ExcRateId = request.args.get("id",None,type=int)
		CurrencyId = request.args.get("currencyId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		ExcRateDate = request.args.get("excRateDate",None,type=str)

		filtering = {"GCRecord": None}

		if ExcRateId:
			filtering["ExcRateId"] = ExcRateId
		if CurrencyId:
			filtering["CurrencyId"] = CurrencyId

		exc_rates = Exc_rate.query.filter_by(**filtering)\
			.options(joinedload(Exc_rate.currency))

		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			exc_rates = exc_rates.filter(Exc_rate.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

		if ExcRateDate:
			if (type(ExcRateDate) != datetime):
				ExcRateDate = dateutil.parser.parse(ExcRateDate)
			exc_rates = exc_rates.filter(Exc_rate.ExcRateDate == ExcRateDate)

		data = []
		for exc_rate in exc_rates.all():
			exc_rate_data = exc_rate.to_json_api()
			exc_rate_data["CurrencyCode"] = exc_rate.currency.CurrencyCode

			data.append(exc_rate_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Exchange rate",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = [] 

		currencies = Currency.query.filter_by(GCRecord = None).all()

		for exc_rate_req in req:
			exc_rate = addExcRateDict(exc_rate_req)

			CurrencyCode = exc_rate_req["CurrencyCode"]
			thisCurrency = [currency.to_json_api() for currency in currencies if currency.CurrencyCode == CurrencyCode]
			exc_rate["CurrencyId"] = thisCurrency[0]["CurrencyId"] if thisCurrency else None

			try:
				filtering = {"GCRecord": None}
				filtering["ExcRateDate"] = dateutil.parser.parse(exc_rate['ExcRateDate']).date()
				thisExcRate = Exc_rate.query\
					.filter_by(**filtering)\
					.first()

				if thisExcRate:
					thisExcRate.update(**exc_rate)
					data.append(exc_rate)
				else:
					thisExcRate = Exc_rate(**exc_rate)
					db.session.add(thisExcRate)
					data.append(exc_rate)

			except Exception as ex:
				print(f"{datetime.now()} | Exc_rate Api Exception: {ex}")
				failed_data.append(exc_rate)

		db.session.commit()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response