# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from flask import current_app
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack import db

from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_
import uuid

from main_pack.models.base.models import Warehouse, Division
from main_pack.models.commerce.models import Res_total,Resource
from main_pack.api.commerce.utils import addResTotalDict

from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-res-totals/",methods=['GET','POST'])
@sha_required
def api_res_totals():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		res_totals = Res_total.query.filter_by(GCRecord = None)
		if DivId:
			res_totals = res_totals.filter_by(DivId = DivId)
		if notDivId:
			res_totals = res_totals.filter(Res_total.DivId != notDivId)
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			res_totals = res_totals.filter(Res_total.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		res_totals = res_totals.all()

		data = []
		for res_total in res_totals:
			res_total_info = res_total.to_json_api()
			res_total_info["WhGuid"] = res_total.warehouse.WhGuid if res_total.warehouse else None
			res_total_info["DivGuid"] = res_total.division.DivGuid if res_total.division else None
			res_total_info["ResGuid"] = res_total.resource.ResGuid if res_total.resource else None
			data.append(res_total_info)

		res = {
			"status": 1,
			"message": "All res totals",
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

			resources = Resource.query\
				.filter_by(GCRecord = None)\
				.filter(Resource.ResGuid != None).all()
			warehouses = Warehouse.query\
				.filter_by(GCRecord = None)\
				.filter(Warehouse.WhGuid != None).all()
			divisions = Division.query\
				.filter_by(GCRecord = None)\
				.filter(Division.DivGuid != None).all()

			division_DivId_list = [division.DivId for division in divisions]
			division_DivGuid_list = [str(division.DivGuid) for division in divisions]

			warehouse_WhId_list = [warehouse.WhId for warehouse in warehouses]
			warehouse_WhGuid_list = [str(warehouse.WhGuid) for warehouse in warehouses]

			resource_ResId_list = [resource.ResId for resource in resources]
			resource_ResGuid_list = [str(resource.ResGuid) for resource in resources]
			res_totals = []
			failed_res_totals = [] 
			for res_total_req in req:
				res_total_info = addResTotalDict(res_total_req)
				
				# sync the pending amount (used by synchronizer)
				res_total_info["ResPendingTotalAmount"] = res_total_info["ResTotBalance"]

				try:
					# handle AkHasap's database exceptions of -1 meaning "all"
					if res_total_info["WhId"] > 0:
						# handling WhId existence exception
						res_total_req["WhId"] = None

						ResRegNo = res_total_req["ResRegNo"]
						ResGuid = res_total_req["ResGuid"]
						DivGuid = res_total_req["DivGuid"]
						WhGuid = res_total_req["WhGuid"]
						# WhGuid = uuid.UUID(res_total_req["WhGuid"]) # used for fetching Wh and Resources
						if not ResRegNo or not ResGuid or not WhGuid:
							raise Exception

						try:
							indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
							DivId = int(indexed_div_id)
						except:
							DivId = None
						try:
							indexed_res_id = resource_ResId_list[resource_ResGuid_list.index(ResGuid)]
							ResId = int(indexed_res_id)
						except:
							ResId = None
						try:
							indexed_wh_id = warehouse_WhId_list[warehouse_WhGuid_list.index(WhGuid)]
							WhId = int(indexed_wh_id)
						except:
							WhId = None

						res_total_info["DivId"] = DivId
						res_total_info["ResId"] = ResId
						res_total_info["WhId"] = WhId

						if not ResId or not WhId or not DivId:
							raise Exception

						thisResTotal = Res_total.query\
							.filter_by(ResId = ResId, WhId = WhId, DivId = DivId)\
							.first()
						if thisResTotal:
							res_total_info["ResTotId"] = thisResTotal.ResTotId
							thisResTotal.update(**res_total_info)
						else:
							try:
								lastTotal = Res_total.query.order_by(Res_total.ResTotId.desc()).first()
								ResTotId = lastTotal.ResTotId+1
							except:
								ResTotId = None
							res_total_info["ResTotId"] = ResTotId
							thisResTotal = Res_total(**res_total_info)
							db.session.add(thisResTotal)
							
						thisResTotal = None
						res_totals.append(res_total_req)
					else:
						raise Exception
				except Exception as ex:
					print(f"{datetime.now()} | Res_total Api Exception: {ex}")
					failed_res_totals.append(res_total_req)
			db.session.commit()
			status = checkApiResponseStatus(res_totals,failed_res_totals)
			res = {
				"data": res_totals,
				"fails": failed_res_totals,
				"success_total": len(res_totals),
				"fail_total": len(failed_res_totals)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)
	return response
