# -*- coding: utf-8 -*-
from flask import jsonify,make_response,request
from flask import current_app
from datetime import datetime

from main_pack.api.commerce import api
from main_pack.config import Config

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
		CName = request.args.get("CName","",type=str)
		CKey = request.args.get("CKey","",type=str)
		company = Company.query\
			.filter_by(CName = CName, CKey = CKey)\
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
					new_company = addCompanyDict(company_req)
					company = Company.query\
						.filter_by(CName = new_company.CName)\
						.first()
					if not company:
						company = Company(**new_company)
						db.session.add(company)
					else:
						company.update(**new_company)
					companies.append(new_company)
				except Exception as ex:
					print(f"{datetime.now()} | Company Api Exception: {ex}")
					failed_companies.append(new_company)
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
		DivName = request.args.get("DivName","",type=str)
		DivKey = request.args.get("DivKey","",type=str)
		division = Division.query\
			.filter_by(DivName = DivName, DivKey = DivKey)\
			.first_or_404()

		division_info = division.to_json_api()
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
			divisions = []
			failed_divisions = []
			for division_req in req:
				try:
					new_division = addDivisionDict(division_req)
					division = Division.query\
						.filter_by(
							DivName = new_division.DivName,
							DivGuid = new_division.DivGuid)\
						.first()
					if not division:
						division = Division(**new_division)
						db.session.add(division)
					else:
						division.update(**new_division)
					divisions.append(new_division)
				except Exception as ex:
					print(f"{datetime.now()} | Division Api Exception: {ex}")
					failed_divisions.append(new_division)
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