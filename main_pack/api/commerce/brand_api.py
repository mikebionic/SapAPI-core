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
	imageList = request.args.get("imageList",0,type=int)

	filtering = {"GCRecord": None}

	if BrandId:
		filtering['BrandId'] = BrandId

	brand_query = Brand.query.filter_by(**filtering)
	if BrandName:
		brand_query = brand_query\
			.filter(BrandName.ilike(f"%{BrandName}%"))
	brand_query = brand_query.options(joinedload(Brand.Image))\
		.order_by(Brand.BrandVisibleIndex.asc())

	brands = brand_query.all()
	data = []
	for brand in brands:
		this_brand_data = brand.to_json_api()
		this_brand_images = [image.to_json_api() for image in brand.Image if not image.GCRecord]
		this_brand_data["FilePath"] = this_brand_images[-1]["FilePath"] if this_brand_images else ""
		if imageList:
			this_brand_data["Images"] = this_brand_images

		data.append(this_brand_data)

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