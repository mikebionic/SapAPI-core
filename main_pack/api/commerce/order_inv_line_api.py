from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Order_inv_line
from main_pack.api.commerce.utils import addOrderInvLineDict
from main_pack import db
from flask import current_app


@api.route("/tbl-dk-order-inv-lines/",methods=['GET','POST','PUT'])
def api_order_inv_lines():
	if request.method == 'GET':
		order_inv_lines = Order_inv_line.query\
			.filter(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None).all()
		res = {
			"status":1,
			"message":"All order inv lines",
			"data":[order_inv_line.to_json_api() for order_inv_line in order_inv_lines],
			"total":len(order_inv_lines)
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
					if not 'OInvLineId' in order_inv_line:
						newOrderInv = Order_inv_line(**order_inv_line)
						db.session.add(newOrderInv)
						db.session.commit()
						order_inv_lines.append(order_inv_line)
					else:
						OInvLineId = order_inv_line['OInvLineId']
						thisOrderInv = Order_inv_line.query.get(int(OInvLineId))
						if thisOrderInv is not None:
							thisOrderInv.update(**order_inv_line)
							db.session.commit()
							order_inv_lines.append(order_inv_line)

						else:
							newOrderInv = Order_inv_line(**order_inv_line)
							db.session.add(newOrderInv)
							db.session.commit()
							order_inv_lines.append(order_inv_line)
				except:
					failed_order_inv_lines.append(order_inv_line)

			status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)
			res = {
				"data":order_inv_lines,
				"fails":failed_order_inv_lines,
				"success_total":len(order_inv_lines),
				"fail_total":len(failed_order_inv_lines)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)
			print(response)

	return response