# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request
from datetime import datetime
from sqlalchemy.orm import joinedload

from . import api
from main_pack import db

from main_pack.api.auth.utils import sha_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json

from main_pack.models import Company, Division
from .utils import addDivisionDict


@api.route("/division/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_division():
	if request.method == 'GET':
		DivGuid = request.args.get("DivGuid",None,type=str)

		filtering = {"GCRecord": None}

		if DivGuid:
			filtering["DivGuid"] = DivGuid

		division = Division.query\
			.filter_by(**filtering)\
			.options(joinedload(Division.company))\
			.first()

		data = {}

		if division:
			data = division.to_json_api()
			data["CGuid"] = division.company.CGuid if division.company and not division.company.GCRecord else None

		res = {
			"status": 1 if data else 0,
			"message": "Division",
			"data": data,
			"total": 1 if data else 0
		}

		status_code = 200 if data else 404
		response = make_response(jsonify(res), status_code)
	
	if request.method == 'POST':
		req = request.get_json()

		companies = Company.query.filter_by(GCRecord = None).all()
		company_CId_list = [company.CId for company in companies]
		company_CGuid_list = [str(company.CGuid) for company in companies]

		data = []
		failed_data = []

		for division_req in req:
			try:
				CGuid = division_req["CGuid"]
				CId = int(company_CId_list[company_CGuid_list.index(CGuid)])

				division_info = addDivisionDict(division_req)
				division_info["CId"] = CId

				division = Division.query\
					.filter_by(
						DivGuid = division_info["DivGuid"],
						GCRecord = None)\
					.first()

				if division:
					division_info["DivId"] = division.DivId
					division.update(**division_info)

				else:
					division = Division(**division_info)
					db.session.add(division)

				data.append(division_req)

			except Exception as ex:
				print(f"{datetime.now()} | Division Api Exception: {ex}")
				failed_data.append(division_req)

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