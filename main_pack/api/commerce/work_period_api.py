# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from datetime import datetime, timedelta
import dateutil.parser

from main_pack import db
from . import api
from .utils import addWorkPeriodDict

from main_pack.models import Currency
from main_pack.models import Work_period

from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json


@api.route("/tbl-dk-work-periods/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_work_periods():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		WpId = request.args.get("id",None,type=int)

		filtering = {"GCRecord": None}

		if WpId:
			filtering["WpId"] = WpId
		if DivId:
			filtering["DivId"] = DivId

		work_periods = Work_period.query.filter_by(**filtering)

		if notDivId:
			work_periods = work_periods.filter(Work_period.DivId != notDivId)

		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			work_periods = work_periods.filter(Barcode.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

		data = [work_period.to_json_api() for work_period in work_periods.all()]

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Work periods",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = []

		currencies = Currency.query.filter_by(GCRecord = None).all()

		for work_period_req in req:
			work_period = addWorkPeriodDict(work_period_req)

			CurrencyCode = work_period_req["CurrencyCode"]
			thisCurrency = [currency.to_json_api() for currency in currencies if currency.CurrencyCode == CurrencyCode]
			work_period["CurrencyId"] = thisCurrency[0]["CurrencyId"] if thisCurrency else None

			try:
				if not 'WpId' in work_period:
					thisWorkPeriod = Work_period(**work_period)
					db.session.add(thisWorkPeriod)
					data.append(work_period)

				else:
					WpId = work_period['WpId']
					thisWorkPeriod = Work_period.query.get(int(WpId))

					if thisWorkPeriod:
						thisWorkPeriod.update(**work_period)
						data.append(work_period)

					else:
						thisWorkPeriod = Work_period(**work_period)
						db.session.add(thisWorkPeriod)
						data.append(work_period)

			except Exception as ex:
				print(f"{datetime.now()} | Work_period Api Exception: {ex}")
				failed_data.append(work_period)

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