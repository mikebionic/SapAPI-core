# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy.orm import joinedload

from main_pack import db
from . import api
from .utils import addWarehouseDict

from main_pack.models.base.models import Warehouse, Division

from main_pack.api.auth.utils import sha_required, token_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json


def get_warehouses(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	WhId = None,
	WhName = None):

	filtering = {"GCRecord": None}

	if WhId:
		filtering["WhId"] = WhId
	if WhName:
		filtering["WhName"] = WhName
	if DivId:
		filtering["DivId"] = DivId

	warehouse_query = Warehouse.query.filter_by(**filtering)\
		.options(
			joinedload(Warehouse.company),
			joinedload(Warehouse.division))

	if notDivId:
		warehouse_query = warehouse_query.filter(Warehouse.DivId != notDivId)

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		warehouse_query = warehouse_query.filter(Warehouse.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	warehouses = warehouse_query.all()

	data = []
	for warehouse in warehouses:
		warehouse_info = warehouse.to_json_api()
		warehouse_info["DivGuid"] = warehouse.division.DivGuid if warehouse.division and not warehouse.division.GCRecord else None
		data.append(warehouse_info)

	return data


@api.route("/v-warehouses/")
@token_required
def api_v_warehouses():
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"WhId": request.args.get("id",None,type=int),
		"WhName": request.args.get("name","",type=str)
	}

	data = get_warehouses(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Warehouses",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)


@api.route("/tbl-dk-warehouses/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_warehouses():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"notDivId": request.args.get("notDivId",None,type=int),
			"synchDateTime": request.args.get("synchDateTime",None,type=str),
			"WhId": request.args.get("id",None,type=int),
			"WhName": request.args.get("name","",type=str)
		}

		data = get_warehouses(**arg_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Warehouses",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		divisions = Division.query.filter_by(GCRecord = None).all()
		division_DivId_list = [division.DivId for division in divisions]
		division_DivGuid_list = [str(division.DivGuid) for division in divisions]
		division_CId_list = [str(division.CId) for division in divisions]

		data = []
		failed_data = []

		for warehouse_req in req:
			try:
				DivGuid = warehouse_req['DivGuid']
				indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
				indexed_c_id = division_CId_list[division_DivGuid_list.index(DivGuid)]

				if not indexed_div_id:
					raise Exception

				if not indexed_c_id:
					raise Exception

				DivId = int(indexed_div_id)
				CId = int(indexed_c_id)

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

				data.append(warehouse_req)

			except Exception as ex:
				print(f"{datetime.now()} | Warehouse Api Exception: {ex}")
				failed_data.append(warehouse_req)

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