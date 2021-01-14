# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from datetime import datetime

from main_pack.models.base.models import Company
from main_pack.models.commerce.models import Brand
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload


@api.route("/tbl-dk-brands/")
def api_brands():
	if request.method == 'GET':
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

		if (not BrandId and not BrandName):
			brands = brand_query.all()
			data = []
			for brand in brands:
				brandList = brand.to_json_api()
				brandList["Images"] = [image.to_json_api() for image in brand.Image if image.GCRecord == None]
				data.append(brandList)
			res = {
				"status": 1 if len(data) > 0 else 0,
				"message": "All view brands",
				"data": data,
				"total": len(data)
			}
			response = make_response(jsonify(res),200)

		else:
			brand = brand_query.first()
			data = []
			status_code = 404
			if brand:
				try:
					data = brand.to_json_api()
					data["Images"] = [image.to_json_api() for image in brand.Image if image.GCRecord == None]
					status_code = 200
				except Exception as ex:
					print(f"{datetime.now()} | brand Api Exception: {ex}")

			res = {
				"status": 1 if len(data) > 0 else 0,
				"message": "Brand",
				"data": data,
				"total": 1
			}
			response = make_response(jsonify(res),status_code)

	return response