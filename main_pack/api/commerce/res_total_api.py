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

from main_pack.models.base.models import Warehouse
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
		res = {
			"status": 1,
			"message": "All res totals",
			"data": [res_total.to_json_api() for res_total in res_totals],
			"total": len(res_totals)
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
			res_totals = []
			failed_res_totals = [] 
			for res_total_req in req:
				res_total = addResTotalDict(res_total_req)
				# sync the pending amount (used by synchronizer)
				res_total['ResPendingTotalAmount'] = res_total['ResTotBalance']
				try:
					# handle AkHasap's database exceptions of -1 meaning "all"
					if res_total['WhId'] > 0:
						# handling WhId existence exception
						res_total_req['WhId'] = None
						ResRegNo = res_total_req['ResRegNo']
						WhGuid = uuid.UUID(res_total_req['WhGuid']) # used for fetching Wh and Resources
						if not ResRegNo or not WhGuid:
							raise Exception

						resource = Resource.query\
							.filter_by(GCRecord = None, ResRegNo = ResRegNo).first()
						warehouse = Warehouse.query\
							.filter_by(GCRecord = None, WhGuid = WhGuid).first()

						if not resource or not warehouse:
							raise Exception

						thisResTotal = Res_total.query\
							.filter_by(ResId = resource.ResId, WhId = warehouse.WhId)\
							.first()

						res_total["ResId"] = resource.ResId
						res_total["WhId"] = warehouse.WhId

						if thisResTotal:
							res_total["ResTotId"] = thisResTotal.ResTotId
							thisResTotal.update(**res_total)
							thisResTotal = None
						else:
							lastTotal = Res_total.query.order_by(Res_total.ResTotId.desc()).first()
							ResTotId = lastTotal.ResTotId+1
							res_total["ResTotId"] = ResTotId
							
							newResTotal = Res_total(**res_total)
							db.session.add(newResTotal)
							
						res_total["WhGuid"] = WhGuid
						res_total["ResRegNo"] = ResRegNo
						res_totals.append(res_total)
						
					else:
						raise Exception
				except Exception as ex:
					print(f"{datetime.now()} | Res_total Api Exception: {ex}")
					failed_res_totals.append(res_total)
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