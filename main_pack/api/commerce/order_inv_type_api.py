from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Order_inv_type
from main_pack.api.commerce.utils import addOrderInvTypeDict
from main_pack import db
from flask import current_app


@api.route("/tbl-dk-order-inv-types/",methods=['GET','POST','PUT'])
def api_order_inv_types():
	if request.method == 'GET':
		order_inv_types = Order_inv_type.query.all()
		res = {
			"status":1,
			"message":"All order inv types",
			"data":[order_inv_type.to_json_api() for order_inv_type in order_inv_types],
			"total":len(order_inv_types)
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
			order_inv_types = []
			failed_order_inv_types = [] 
			for order_inv_type in req:
				order_inv_type = addOrderInvTypeDict(order_inv_type)
				try:
					if not 'OInvTypeId' in order_inv_type:
						newOrderInv = Order_inv_type(**order_inv_type)
						db.session.add(newOrderInv)
						db.session.commit()
						order_inv_types.append(order_inv_type)
					else:
						OInvTypeId = order_inv_type['OInvTypeId']
						thisOrderInv = Order_inv_type.query.get(int(OInvTypeId))
						if thisOrderInv is not None:
							thisOrderInv.update(**order_inv_type)
							db.session.commit()
							order_inv_types.append(order_inv_type)

						else:
							newOrderInv = Order_inv_type(**order_inv_type)
							db.session.add(newOrderInv)
							db.session.commit()
							order_inv_types.append(order_inv_type)
				except:
					failed_order_inv_types.append(order_inv_type)

			status = checkApiResponseStatus(order_inv_types,failed_order_inv_types)
			res = {
				"data":order_inv_types,
				"fails":failed_order_inv_types,
				"success_total":len(order_inv_types),
				"fail_total":len(failed_order_inv_types)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)
			print(response)

	return response