# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.config import Config

from main_pack.models.commerce.models import Payment_type, Payment_method


@api.route("/tbl-dk-payment-types/")
def api_paynemt_types():
	payment_types = Payment_type.query\
		.filter_by(GCRecord = None)\
		.filter(Payment_type.PtVisibleIndex != 0)\
		.order_by(Payment_type.PtVisibleIndex.asc())\
		.all()
	res = {
		"status": 1,
		"message": "Payment types",
		"data": [payment_type.to_json_api() for payment_type in payment_types if payment_type.PtVisibleIndex != 0],
		"total": len(payment_types)
	}
	response = make_response(jsonify(res),200)
	return response


@api.route("/tbl-dk-payment-methods/")
def api_payment_methods():
	payment_methods = Payment_method.query\
		.filter_by(GCRecord = None)\
		.filter(Payment_method.PmVisibleIndex != 0)\
		.order_by(Payment_method.PmVisibleIndex.asc())\
		.all()
	res = {
		"status": 1,
		"message": "Payment methods",
		"data": [payment_method.to_json_api() for payment_method in payment_methods if payment_method.PmVisibleIndex != 0],
		"total": len(payment_methods)
	}
	response = make_response(jsonify(res),200)
	return response