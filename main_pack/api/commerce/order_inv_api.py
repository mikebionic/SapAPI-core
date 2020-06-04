from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Order_inv
from main_pack.api.commerce.utils import addOrderInvDict
from main_pack import db
from flask import current_app


@api.route("/tbl-dk-order-invoices/",methods=['GET','POST','PUT'])
def api_order_invoices():
	if request.method == 'GET':
		order_invoices = Order_inv.query.all()
		res = {
			"status":1,
			"message":"All order invoices",
			"data":[order_invoice.to_json_api() for order_invoice in order_invoices],
			"total":len(order_invoices)
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
			order_invoices = []
			failed_order_invoices = [] 
			for order_invoice in req:
				order_invoice = addOrderInvDict(order_invoice)
				try:
					if not 'OInvId' in order_invoice:
						newOrderInv = Order_inv(**order_invoice)
						db.session.add(newOrderInv)
						db.session.commit()
						order_invoices.append(order_invoice)
					else:
						OInvId = order_invoice['OInvId']
						thisOrderInv = Order_inv.query.get(int(OInvId))
						if thisOrderInv is not None:
							thisOrderInv.update(**order_invoice)
							db.session.commit()
							order_invoices.append(order_invoice)

						else:
							newOrderInv = Order_inv(**order_invoice)
							db.session.add(newOrderInv)
							db.session.commit()
							order_invoices.append(order_invoice)
				except:
					failed_order_invoices.append(order_invoice)

			status = checkApiResponseStatus(order_invoices,failed_order_invoices)
			res = {
				"data":order_invoices,
				"fails":failed_order_invoices,
				"success_total":len(order_invoices),
				"fail_total":len(failed_order_invoices)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)
			print(response)

	return response