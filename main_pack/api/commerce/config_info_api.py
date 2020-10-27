# -*- coding: utf-8 -*-
from flask import jsonify,make_response,request
from flask import current_app
from datetime import datetime
import uuid

from main_pack.api.commerce import api
from main_pack.config import Config
from main_pack import db

from main_pack.api.auth.api_login import sha_required
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.base.models import Company, Division
from main_pack.api.commerce.utils import addCompanyDict,addDivisionDict

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

	response = make_response(jsonify(res),200)
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
	response = make_response(jsonify(res),200)
	return response


@api.route("/company/", methods=['GET','POST'])
@sha_required
def api_company():
	if request.method == 'GET':
		CGuid = request.args.get("CGuid","",type=str)
		company = Company.query\
			.filter_by(CGuid = CGuid, GCRecord = None)\
			.first_or_404()

		company_info = company.to_json_api()
		status_code = 200

		res = {
			"status": 1,
			"message": "Company information",
			"data": company_info,
			"total": 1
		}
		response = make_response(jsonify(res),status_code)

	if request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			companies = []
			failed_companies = []
			for company_req in req:
				try:
					company_data = addCompanyDict(company_req)
					company = Company.query\
						.filter_by(
							CGuid = company_data['CGuid'],
							GCRecord = None)\
						.first()
					if company:
						company_data['CId'] = company.CId
						company.update(**company_data)
					else:
						company = Company(**company_data)
						db.session.add(company)
					companies.append(company_data)
				except Exception as ex:
					print(f"{datetime.now()} | Company Api Exception: {ex}")
					failed_companies.append(company_req)
			db.session.commit()
			status = checkApiResponseStatus(companies,failed_companies)
			res = {
				"data": companies,
				"fails": failed_companies,
				"success_total": len(companies),
				"fail_total": len(failed_companies)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)	
	return response


@api.route("/division/",methods=['GET','POST'])
@sha_required
def api_division():
	if request.method == 'GET':
		DivGuid = request.args.get("DivGuid","",type=str)
		division = Division.query\
			.filter_by(DivGuid = DivGuid, GCRecord = None)\
			.first_or_404()

		division_info = division.to_json_api()
		division_info["CGuid"] = division.company.CGuid if division.company else None
		status_code = 200
		res = {
			"status": 1,
			"message": "Division information",
			"data": division_info,
			"total": 1
		}
		response = make_response(jsonify(res),status_code)
	
	if request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			companies = Company.query.filter_by(GCRecord = None).all()
			company_CId_list = [company.CId for company in companies]
			company_CGuid_list = [str(company.CGuid) for company in companies]
			divisions = []
			failed_divisions = []
			for division_req in req:
				try:
					CGuid = division_req["CGuid"]
					indexed_c_id = company_CId_list[company_CGuid_list.index(CGuid)]
					CId = int(indexed_c_id)
					division_info = addDivisionDict(division_req)
					division_info["CId"] = CId
					division = Division.query\
						.filter_by(
							DivGuid = division_info["DivGuid"],
							GCRecord = None)\
						.first()
					if division:
						division['DivId'] = division.DivId
						division.update(**division_info)
					else:
						division = Division(**division_info)
						db.session.add(division)
					divisions.append(division_req)
				except Exception as ex:
					print(f"{datetime.now()} | Division Api Exception: {ex}")
					failed_divisions.append(division_req)
			db.session.commit()
			status = checkApiResponseStatus(divisions,failed_divisions)
			res = {
				"data": divisions,
				"fails": failed_divisions,
				"success_total": len(divisions),
				"fail_total": len(failed_divisions)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)	
	return response