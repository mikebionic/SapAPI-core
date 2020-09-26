# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from datetime import datetime

from main_pack.models.base.models import Company,Sl_image,Slider
from sqlalchemy import or_, and_
# from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-sliders/")
def api_sliders():
	sliders = Slider.query.filter_by(GCRecord = None).all()
	if request.method == 'GET':
		data = []
		for slider in sliders:
			sliderList = slider.to_json_api()
			sliderList["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if sl_image.GCRecord == None]
			data.append(sliderList)
		res = {
			"status": 1,
			"message": "All view sliders",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res),200)
	return response


@api.route("/tbl-dk-sliders/<SlName>/")
def api_slider_info(SlName):
	slider = Slider.query\
		.filter_by(GCRecord = None, SlName = SlName)\
		.first()
	try:
		data = slider.to_json_api()
		data["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if sl_image.GCRecord == None]
		status_code = 200
	except Exception as ex:
		print(f"{datetime.now()} | Slider Api Exception: {ex}")
		data = []
		status_code = 404
		
	res = {
		"status": 1,
		"message": "Slider",
		"data": data,
		"total": 1
	}
	response = make_response(jsonify(res),status_code)
	return response