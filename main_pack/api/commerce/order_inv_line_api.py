# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime

from main_pack.models.commerce.models import Order_inv_line
from main_pack.api.commerce.utils import addOrderInvLineDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-order-inv-lines/",methods=['GET','POST'])
@sha_required
def api_order_inv_lines():
	if request.method == 'GET':
		order_inv_lines = Order_inv_line.query.filter_by(GCRecord = None).all()
		res = {
			"status": 1,
			"message": "All order inv lines",
			"data": [order_inv_line.to_json_api() for order_inv_line in order_inv_lines],
			"total": len(order_inv_lines)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			order_inv_lines = []
			failed_order_inv_lines = [] 
			for order_inv_line in req:
				order_inv_line = addOrderInvLineDict(order_inv_line)
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
			response = make_response(jsonify(res),200)

	return response