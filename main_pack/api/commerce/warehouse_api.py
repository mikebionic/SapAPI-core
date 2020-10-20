# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.base.models import Warehouse
from main_pack.api.commerce.utils import addWarehouseDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-warehouses/",methods=['GET','POST'])
@sha_required
def api_warehouses():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		warehouses = Warehouse.query.filter_by(GCRecord = None)
		if DivId:
			warehouses = warehouses.filter_by(DivId = DivId)
		if notDivId:
			warehouses = warehouses.filter(Warehouse.DivId != notDivId)
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			warehouses = warehouses.filter(Warehouse.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		warehouses = warehouses.all()
		res = {
			"status": 1,
			"message": "All warehouses",
			"data": [warehouse.to_json_api() for warehouse in warehouses],
			"total": len(warehouses)
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
			warehouses = []
			failed_warehouses = []
			# !!! Todo: add DivGuid checkup
			for warehouse_req in req:
				try:
					warehouse_info = addWarehouseDict(warehouse_req)
					warehouse = Warehouse.query\
						.filter_by(
							WhGuid = warehouse_info['WhGuid'])\
						.first()
					if warehouse:
						warehouse.update(**warehouse_info)
					else:
						warehouse = Warehouse(**warehouse_info)
						db.session.add(warehouse)
					warehouses.append(warehouse_info)
				except Exception as ex:
					print(f"{datetime.now()} | Warehouse Api Exception: {ex}")
					failed_warehouses.append(warehouse_req)
			db.session.commit()
			status = checkApiResponseStatus(warehouses,failed_warehouses)
			res = {
				"data": warehouses,
				"fails": failed_warehouses,
				"success_total": len(warehouses),
				"fail_total": len(failed_warehouses)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)
			
	return response