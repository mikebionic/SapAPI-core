# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime

from main_pack import db
from . import api

# orders and db methods
from main_pack.models import Order_inv_type
from .utils import addOrderInvTypeDict
from main_pack.base.apiMethods import checkApiResponseStatus
# / orders and db methods /

from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json


@api.route("/tbl-dk-order-inv-types/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_order_inv_types():
	if request.method == 'GET':
		order_inv_types = Order_inv_type.query.filter_by(GCRecord = None).all()
		data = [order_inv_type.to_json_api() for order_inv_type in order_inv_types]

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Order inv types",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = [] 

		for order_inv_type_req in req:
			order_inv_type = addOrderInvTypeDict(order_inv_type_req)
			try:
				if not 'OInvTypeId' in order_inv_type:
					newOrderInv = Order_inv_type(**order_inv_type)
					db.session.add(newOrderInv)
					data.append(order_inv_type)

				else:
					OInvTypeId = order_inv_type['OInvTypeId']
					thisOrderInv = Order_inv_type.query.get(int(OInvTypeId))

					if thisOrderInv is not None:
						thisOrderInv.update(**order_inv_type)
						data.append(order_inv_type)

					else:
						newOrderInv = Order_inv_type(**order_inv_type)
						db.session.add(newOrderInv)
						data.append(order_inv_type)

			except Exception as ex:
				print(f"{datetime.now()} | OInv_type Api Exception: {ex}")
				failed_data.append(order_inv_type)

		db.session.commit()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response