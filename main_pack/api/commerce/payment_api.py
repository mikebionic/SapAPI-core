# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from . import api
from main_pack.config import Config
from main_pack.models import Payment_type, Payment_method


@api.route("/tbl-dk-payment-types/")
def api_paynemt_types():
	payment_types = Payment_type.query\
		.filter_by(GCRecord = None)\
		.filter(Payment_type.PtVisibleIndex != 0)\
		.order_by(Payment_type.PtVisibleIndex.asc())\
		.all()

	data = [payment_type.to_json_api() for payment_type in payment_types if payment_type.PtVisibleIndex != 0]

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Payment types",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)
	return response


@api.route("/tbl-dk-payment-methods/")
def api_payment_methods():
	payment_methods = Payment_method.query\
		.filter_by(GCRecord = None)\
		.filter(Payment_method.PmVisibleIndex != 0)\
		.order_by(Payment_method.PmVisibleIndex.asc())\
		.all()

	data = [payment_method.to_json_api() for payment_method in payment_methods if payment_method.PmVisibleIndex != 0]

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Payment methods",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)
	return response