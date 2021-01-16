# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from datetime import datetime, timedelta
import dateutil.parser

from main_pack import db
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Work_period
from main_pack.api.commerce.utils import addWorkPeriodDict

from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json


@api.route("/tbl-dk-work-periods/",methods=['GET','POST'])
@sha_required
@request_is_json
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

		work_periods = []
		failed_work_periods = [] 

		for work_period_req in req:
			work_period = addWorkPeriodDict(work_period_req)
			try:
				if not 'WpId' in work_period:
					newWorkPeriod = Work_period(**work_period)
					db.session.add(newWorkPeriod)
					work_periods.append(work_period)

				else:
					WpId = work_period['WpId']
					thisWorkPeriod = Work_period.query.get(int(WpId))

					if thisWorkPeriod is not None:
						thisWorkPeriod.update(**work_period)
						work_periods.append(work_period)

					else:
						newWorkPeriod = Work_period(**work_period)
						db.session.add(newWorkPeriod)
						work_periods.append(work_period)

			except Exception as ex:
				print(f"{datetime.now()} | Work_period Api Exception: {ex}")
				failed_work_periods.append(work_period)

		db.session.commit()
		status = checkApiResponseStatus(work_periods,failed_work_periods)

		res = {
			"data": work_periods,
			"fails": failed_work_periods,
			"success_total": len(work_periods),
			"fail_total": len(failed_work_periods)
		}
		for e in status:
			res[e] = status[e]
		response = make_response(jsonify(res), 200)
			
	return response