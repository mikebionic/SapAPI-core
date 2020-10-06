# -*- coding: utf-8 -*-
from flask import jsonify,make_response,request
from main_pack.api.commerce import api
from flask import current_app
from main_pack.config import Config
from main_pack.models.base.models import Company, Division

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


@api.route("/company/")
def api_company():
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
	return response

@api.route("/division/")
def api_division():
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
	return response