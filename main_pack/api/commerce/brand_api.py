# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from sqlalchemy.orm import joinedload

from . import api

from main_pack.models import Brand
from main_pack.commerce.commerce.utils import UiBrandsList

@api.route("/tbl-dk-brands/")
def api_brands():
	BrandId = request.args.get("id",None,type=int)
	BrandName = request.args.get("name","",type=str)

	filtering = {"GCRecord": None}

	if BrandId:
		filtering['BrandId'] = BrandId
	if BrandName:
		filtering['BrandName'] = BrandName

	brand_query = Brand.query\
		.filter_by(**filtering)\
		.options(joinedload(Brand.Image))

	brands = brand_query.all()
	data = []
	for brand in brands:
		brandList = brand.to_json_api()
		brandList["Images"] = [image.to_json_api() for image in brand.Image if not image.GCRecord]
		data.append(brandList)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Brands",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/v-brands/")
def api_v_brands():
	res = UiBrandsList()
	return res