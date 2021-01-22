# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request, abort
from flask import current_app
from datetime import datetime
import uuid
from sqlalchemy.orm import joinedload

from main_pack.api.commerce import api
from main_pack.config import Config
from main_pack import db

from main_pack.api.auth.utils import sha_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json

from main_pack.models.base.models import Company, Division
from main_pack.api.commerce.utils import addCompanyDict, addDivisionDict

@api.route("/api-config/")
def api_config():
	config_data = {
		"NEGATIVE_WH_QTY_SALE": Config.NEGATIVE_WH_QTY_SALE,
		"NEGATIVE_WH_QTY_ORDER": Config.NEGATIVE_WH_QTY_ORDER,
		"SHOW_NEGATIVE_WH_QTY_RESOURCE": Config.SHOW_NEGATIVE_WH_QTY_RESOURCE,
		# "PRICE_2_TEXT_LANGUAGE": Config.PRICE_2_TEXT_LANGUAGE,
		# "PRICE_2_TEXT_CURRENCY": Config.PRICE_2_TEXT_CURRENCY
	}
	res = {
		"status": 1,
		"message": "Api configurations",
	}
	for data in config_data:
		res[data] = config_data[data]

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
@sha_required
@request_is_json
def api_company():
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


@api.route("/division/",methods=['GET','POST'])
@sha_required
@request_is_json
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