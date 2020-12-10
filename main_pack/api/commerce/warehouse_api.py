# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.base.models import Warehouse,Division
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
		warehouse_query = Warehouse.query.filter_by(GCRecord = None)
		if DivId:
			warehouse_query = warehouse_query.filter_by(DivId = DivId)
		if notDivId:
			warehouse_query = warehouse_query.filter(Warehouse.DivId != notDivId)
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			warehouse_query = warehouse_query.filter(Warehouse.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		warehouse_query = warehouse_query.all()

		data = []
		for warehouse in warehouse_query:
			warehouse_info = warehouse.to_json_api()
			warehouse_info["DivGuid"] = warehouse.division.DivGuid if warehouse.division else None
			data.append(warehouse_info)
		res = {
			"status": 1,
			"message": "All warehouses",
			"data": data,
			"total": len(data)
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
			divisions = Division.query.filter_by(GCRecord = None).all()
			division_DivId_list = [division.DivId for division in divisions]
			division_DivGuid_list = [str(division.DivGuid) for division in divisions]
			division_CId_list = [str(division.CId) for division in divisions]

			warehouses = []
			failed_warehouses = []
			for warehouse_req in req:
				try:
					DivGuid = warehouse_req['DivGuid']
					indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
					indexed_c_id = division_CId_list[division_DivGuid_list.index(DivGuid)]
					if not indexed_div_id:
						raise Exception
					DivId = int(indexed_div_id)

					warehouse_info = addWarehouseDict(warehouse_req)
					warehouse_info['DivId'] = DivId
					warehouse_info['CId'] = CId
					warehouse = Warehouse.query\
						.filter_by(
							WhGuid = warehouse_info['WhGuid'])\
						.first()
					if warehouse:
						warehouse_info['WhId'] = warehouse.WhId
						warehouse.update(**warehouse_info)
					else:
						warehouse = Warehouse(**warehouse_info)
						db.session.add(warehouse)
					warehouses.append(warehouse_req)
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