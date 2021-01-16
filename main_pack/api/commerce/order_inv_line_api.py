# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime

from main_pack import db
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Order_inv_line
from main_pack.api.commerce.utils import addOrderInvLineDict

from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus


@api.route("/tbl-dk-order-inv-lines/",methods=['GET','POST'])
@sha_required
@request_is_json
def api_order_inv_lines():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)

		order_inv_lines = Order_inv_line.query.filter_by(GCRecord = None)

		if DivId:
			order_inv_lines = order_inv_lines.filter_by(DivId = DivId)
		if notDivId:
			order_inv_lines = order_inv_lines.filter(Order_inv_line.notDivId != notDivId)

		data = [order_inv_line.to_json_api() for order_inv_line in order_inv_lines.all()]

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Order inv lines",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		order_inv_lines = []
		failed_order_inv_lines = [] 

		for order_inv_line_req in req:
			order_inv_line = addOrderInvLineDict(order_inv_line_req)
			try:
				OInvLineId = order_inv_line['OInvLineId']
				thisOrderInv = Order_inv_line.query.get(int(OInvLineId))

				if thisOrderInv:
					thisOrderInv.update(**order_inv_line)
					order_inv_lines.append(order_inv_line)

				else:
					newOrderInv = Order_inv_line(**order_inv_line)
					db.session.add(newOrderInv)
					order_inv_lines.append(order_inv_line)

			except Exception as ex:
				print(f"{datetime.now()} | OInvLine Exception: {ex}")
				failed_order_inv_lines.append(order_inv_line)

		db.session.commit()
		status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)

		res = {
			"data": order_inv_lines,
			"fails": failed_order_inv_lines,
			"success_total": len(order_inv_lines),
			"fail_total": len(failed_order_inv_lines)
		}
		for e in status:
			res[e] = status[e]
		response = make_response(jsonify(res), 200)

	return response