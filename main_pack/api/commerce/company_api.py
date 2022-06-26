# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime
from sqlalchemy.orm import joinedload

from . import api
from main_pack import db

from main_pack.models import (
	Company,
	Bank,
	Accounting_info
)
from main_pack.api.auth.utils import token_required, admin_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json
from .utils import addCompanyDict


@api.route("/v-company/",methods=['GET'])
@token_required
def api_v_company(user):

	company = Company.query\
		.filter_by(GCRecord = None)\
		.options(
			joinedload(Company.Accounting_info)\
				.options(joinedload(Accounting_info.bank)))\
		.first()

	data = {}
	if company:
		data = company.to_json_api()

		accounting_data = []
		for accounting_info in company.Accounting_info:
			if not accounting_info.GCRecord:
				info = accounting_info.to_json_api()
				info["Bank"] = accounting_info.bank.to_json_api() if accounting_info.bank and not accounting_info.bank.GCRecord else {}

			accounting_data.append(info)

		data["Accounting_info"] = accounting_data

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Company",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/company-info/")
def api_company_info():
	company = Company.query.first()
	company_info = company.to_json_api()
	res = {
		"status": 1,
		"message": "Company information",
		"data": company_info,
		"total": 1
	}
	response = make_response(jsonify(res), 200)
	return response


@api.route("/company/", methods=['GET','POST'])
@admin_required
@request_is_json(request)
def api_company(user):
	if request.method == 'GET':
		CGuid = request.args.get("CGuid",None,type=str)

		filtering = {"GCRecord": None}

		if CGuid:
			filtering["CGuid"] = CGuid

		company = Company.query.filter_by(**filtering).first_or_404()

		data = company.to_json_api() if company else {}

		res = {
			"status": 1 if data else 0,
			"message": "Company information",
			"data": data,
			"total": 1 if data else 0
		}

		status_code = 200 if data else 404
		response = make_response(jsonify(res), status_code)

	if request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = []

		for company_req in req:
			try:
				company_info = addCompanyDict(company_req)
				company = Company.query\
					.filter_by(
						CGuid = company_info["CGuid"],
						GCRecord = None)\
					.first()

				if company:
					company_info["CId"] = company.CId
					company.update(**company_info)

				else:
					company = Company(**company_info)
					db.session.add(company)

				data.append(company_info)

			except Exception as ex:
				print(f"{datetime.now()} | Company Api Exception: {ex}")
				failed_data.append(company_req)

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