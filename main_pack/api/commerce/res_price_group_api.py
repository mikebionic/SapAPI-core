# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack import db
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Res_price_group
from main_pack.api.auth.utils import token_required


@api.route("/tbl-dk-res-price-groups/",methods=['GET'])
@token_required
def api_res_price_groups():
	ResPriceGroupId = request.args.get("id",None,type=int)
	UsageStatusId = request.args.get("usageStatus",None,type=int)
	ResPriceGroupName = request.args.get("name",None,type=str)
	FromResPriceTypeId = request.args.get("fromPriceType",None,type=int)
	ToResPriceTypeId = request.args.get("toPriceType",None,type=int)

	filtering = {"GCRecord": None}

	if ResPriceGroupId:
		filtering["ResPriceGroupId"] = ResPriceGroupId
	if UsageStatusId:
		filtering["UsageStatusId"] = UsageStatusId
	if ResPriceGroupName:
		filtering["ResPriceGroupName"] = ResPriceGroupName
	if FromResPriceTypeId:
		filtering["FromResPriceTypeId"] = FromResPriceTypeId
	if ToResPriceTypeId:
		filtering["ToResPriceTypeId"] = ToResPriceTypeId

	res_price_groups = Res_price_group.query.filter_by(**filtering).all()

	data = [res_price_group.to_json_api() for res_price_group in res_price_groups]

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All res prices",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response