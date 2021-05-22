# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify
from datetime import datetime

from main_pack.api.v1.image_api import api
from main_pack.api.v1.image_api.utils import get_images


@api.route("/v-images-by-excluded-list/", methods=['POST'])
def v_image_by_excluded_list_post():
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"EmpId": request.args.get("empId",None,type=int),
		"BrandId": request.args.get("brandId",None,type=int),
		"CId": request.args.get("companyId",None,type=int),
		"UId": request.args.get("userId",None,type=int),
		"RpAccId": request.args.get("rpAccId",None,type=int),
		"ResId": request.args.get("resId",None,type=int),
		"ResCatId": request.args.get("categoryId",None,type=int),
		"ProdId": request.args.get("prodId",None,type=int),
		"users": request.args.get("users",None,type=int),
		"brands": request.args.get("brands",None,type=int),
		"resources": request.args.get("resources",None,type=int),
		"rp_accs": request.args.get("rp_accs",None,type=int),
		"prods": request.args.get("prods",None,type=int),
		"employees": request.args.get("employees",None,type=int),
		"categories": request.args.get("categories",None,type=int),
		"companies": request.args.get("companies",None,type=int)
	}

	data = []
	req = request.get_json()
	try:
		arg_data["images_to_exclude"] = req if req else None
		data = get_images(**arg_data)

	except Exception as ex:
		print(f"{datetime.now()} | v-image by excluded list Exception: {ex}")

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All images",
		"data": data,
		"total": len(data)
	}

	return make_response(jsonify(res), 200)