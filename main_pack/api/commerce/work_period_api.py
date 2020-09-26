# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime

from main_pack.models.commerce.models import Work_period
from main_pack.api.commerce.utils import addWorkPeriodDict
from main_pack import db
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-work-periods/",methods=['GET','POST'])
@sha_required
def api_work_periods():
	if request.method == 'GET':
		work_periods = Work_period.query\
			.filter(Work_period.GCRecord=='' or Work_period.GCRecord==None).all()
		res = {
			"status": 1,
			"message": "All work periods",
			"data": [work_period.to_json_api() for work_period in work_periods],
			"total": len(work_periods)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			work_periods = []
			failed_work_periods = [] 
			for work_period in req:
				work_period = addWorkPeriodDict(work_period)
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
			response = make_response(jsonify(res),200)
			
	return response