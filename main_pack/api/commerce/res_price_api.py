# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime
from sqlalchemy import and_

from main_pack.models.commerce.models import Res_price, Resource
from main_pack.api.commerce.utils import addResPriceDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-res-prices/",methods=['GET','POST','PUT'])
@sha_required
def api_res_prices():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		res_prices = Res_price.query.filter_by(GCRecord = None)
		if DivId:
			res_prices = res_prices\
				.join(Resource, and_(
					Resource.ResId == Res_price.ResId,
					Resource.DivId == DivId))
		if notDivId:
			res_prices = res_prices\
				.join(Resource, and_(
					Resource.ResId == Res_price.ResId,
					Resource.DivId != notDivId))

		res_prices = res_prices.all()
		res = {
			"status": 1,
			"message": "All res prices",
			"data": [res_price.to_json_api() for res_price in res_prices],
			"total": len(res_prices)
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
			res_prices = []
			failed_res_prices = [] 
			for res_price_req in req:
				res_price = addResPriceDict(res_price_req)
				try:
					ResRegNo = res_price_req['ResRegNo']
					ResPriceRegNo = res_price_req['ResPriceRegNo']
					if not ResRegNo or not ResPriceRegNo:
						raise Exception

					resource = Resource.query\
						.filter_by(GCRecord = None, ResRegNo = ResRegNo).first()
					if not resource:
						raise Exception

					thisResPrice = Res_price.query\
						.filter_by(
							GCRecord = None,
							ResPriceRegNo = ResPriceRegNo)\
						.first()

					res_price['ResId'] = resource.ResId

					if thisResPrice:
						thisResPrice.update(**res_price)
					else:
						thisResPrice = Res_price(**res_price)
						db.session.add(thisResPrice)
					thisResPrice = None
					
					res_price["ResRegNo"] = ResRegNo
					res_price["ResPriceRegNo"] = ResRegNo
					res_prices.append(res_price)

				except Exception as ex:
					print(f"{datetime.now()} | Res_price Api Exception: {ex}")
					failed_res_prices.append(res_price_req)

			status = checkApiResponseStatus(res_prices,failed_res_prices)
			res = {
				"data": res_prices,
				"fails": failed_res_prices,
				"success_total": len(res_prices),
				"fail_total": len(failed_res_prices)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),200)
	return response