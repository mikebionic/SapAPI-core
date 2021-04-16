# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from . import api
from main_pack.models import Payment_type
from main_pack.api.common import get_payment_types, get_payment_methods


@api.route("/tbl-dk-payment-types/")
def api_paynemt_types():

	data = get_payment_types()

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

	data = get_payment_methods()

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Payment methods",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)
	return response