# -*- coding: utf-8 -*-
from flask import jsonify, make_response

from . import api
from main_pack.config import Config


@api.route("/api-config/")
def api_config():
	config_data = {
		"NEGATIVE_WH_QTY_SALE": bool(Config.NEGATIVE_WH_QTY_SALE),
		"NEGATIVE_WH_QTY_ORDER": bool(Config.NEGATIVE_WH_QTY_ORDER),
		"SHOW_NEGATIVE_WH_QTY_RESOURCE": bool(Config.SHOW_NEGATIVE_WH_QTY_RESOURCE),
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