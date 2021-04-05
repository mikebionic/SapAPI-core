# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session

from main_pack.config import Config
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack import db, cache
from . import api
from .utils import addResPriceDict

from main_pack.models import Res_price, Resource, Res_price_group

from main_pack.api.auth.utils import sha_required, token_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.priceMethods import calculatePriceByGroup
from main_pack.base.apiMethods import checkApiResponseStatus


def get_res_prices(
	DivId = None,
	notDivId = None,
	ResPriceTypeId = None,
	ResPriceGroupId = None):

	res_price_groups = Res_price_group.query.filter_by(GCRecord = None).all()

	filtering = {"GCRecord": None}

	if ResPriceTypeId:
		filtering["ResPriceTypeId"] = ResPriceTypeId

	res_prices = Res_price.query\
		.filter_by(**filtering)\
		.options(joinedload(Res_price.resource))

	if DivId:
		res_prices = res_prices\
			.join(Resource, and_(
				Resource.ResId == Res_price.ResId,
				Resource.DivId == DivId,
				Resource.GCRecord == None))

	if notDivId:
		res_prices = res_prices\
			.join(Resource, and_(
				Resource.ResId == Res_price.ResId,
				Resource.DivId != notDivId,
				Resource.GCRecord == None))

	res_prices = res_prices.all()


	data = []
	for res_price in res_prices:
		try:
			List_Res_price = calculatePriceByGroup(
				ResPriceGroupId = ResPriceGroupId,
				Res_price_dbModels = [res_price],
				Res_pice_group_dbModels = res_price_groups)

			if not List_Res_price:
				raise Exception

			res_price_info = List_Res_price[0]
			res_price_info["ResGuid"] = res_price.resource.ResGuid if res_price.resource and not res_price.resource.GCRecord else None
			res_price_info["ResRegNo"] = res_price.resource.ResRegNo if res_price.resource and not res_price.resource.GCRecord else None
			data.append(res_price_info)

		except Exception as ex:
			print(f"{datetime.now()} | Res_price fetch function Exception: {ex}")

	return data


@api.route("/v-res-prices/")
@token_required
def api_v_res_prices(user):
	current_user = user["current_user"]
	model_type = user["model_type"]

	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"ResPriceTypeId": request.args.get("priceType",2,type=int)
	}

	ResPriceGroupId = Config.DEFAULT_RES_PRICE_GROUP_ID if Config.DEFAULT_RES_PRICE_GROUP_ID > 0 else None
	if current_user:
		if (model_type != "device"):
			ResPriceGroupId = current_user.ResPriceGroupId if current_user.ResPriceGroupId else None
		else:
			ResPriceGroupId = current_user.user.ResPriceGroupId if current_user.user else None

	elif "ResPriceGroupId" in session:
		ResPriceGroupId = session["ResPriceGroupId"]

	arg_data["ResPriceGroupId"] = ResPriceGroupId

	data = get_res_prices(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All res prices",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/tbl-dk-res-prices/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_res_prices():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"notDivId": request.args.get("notDivId",None,type=int),
			"ResPriceTypeId": request.args.get("priceType",None,type=int),
			"ResPriceGroupId": request.args.get("priceGroup",None,type=int)
		}

		data = get_res_prices(**arg_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "All res prices",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()
	
		resources = Resource.query\
			.filter_by(GCRecord = None)\
			.filter(Resource.ResGuid != None).all()

		resource_ResId_list = [resource.ResId for resource in resources]
		resource_ResGuid_list = [str(resource.ResGuid) for resource in resources]

		data = []
		failed_data = [] 

		for res_price_req in req:
			res_price_info = addResPriceDict(res_price_req)
			try:
				ResRegNo = res_price_req['ResRegNo']
				ResGuid = res_price_req['ResGuid']
				ResPriceRegNo = res_price_req['ResPriceRegNo']
				
				try:
					indexed_res_id = resource_ResId_list[resource_ResGuid_list.index(ResGuid)]
					ResId = int(indexed_res_id)
				except:
					ResId = None

				if not ResId or not ResPriceRegNo:
					raise Exception

				res_price_info["ResId"] = ResId
				ResPriceTypeId = res_price_info["ResPriceTypeId"]
				thisResPrice = Res_price.query\
					.filter_by(
						GCRecord = None,
						ResPriceTypeId = ResPriceTypeId,
						ResId = ResId,
						ResPriceRegNo = ResPriceRegNo)\
					.first()

				if thisResPrice:
					res_price_info["ResPriceId"] = thisResPrice.ResPriceId
					thisResPrice.update(**res_price_info)

				else:
					try:
						lastPrice = Res_price.query.order_by(Res_price.ResPriceId.desc()).first()
						ResPriceId = lastPrice.ResPriceId + 1
					except:
						ResPriceId = None
					res_price_info["ResPriceId"] = ResPriceId

					thisResPrice = Res_price(**res_price_info)
					db.session.add(thisResPrice)

				thisResPrice = None
				data.append(res_price_req)

			except Exception as ex:
				print(f"{datetime.now()} | Res_price Api Exception: {ex}")
				failed_data.append(res_price_req)

		db.session.commit()
		cache.clear()
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