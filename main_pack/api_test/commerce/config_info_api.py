# -*- coding: utf-8 -*-
from flask import jsonify,make_response
from main_pack.api_test.commerce import api
from flask import current_app
from main_pack.config import Config
from main_pack.models.base.models import Company

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
	company = Company.query.get(1)
	company_info = company.to_json_api()
	res = {
		"status": 1,
		"message": "Company information",
		"data": company_info
	}
	response = make_response(jsonify(res),200)
	return response