# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from datetime import datetime

from main_pack.models.base.models import Company,Sl_image,Slider
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload


@api.route("/tbl-dk-sliders/")
def api_sliders():
	DivId = request.args.get("DivId",None,type=int)
	notDivId = request.args.get("notDivId",None,type=int)
	sliders = Slider.query.filter_by(GCRecord = None)
	if DivId:
		sliders = sliders.filter_by(DivId = DivId)
	if notDivId:
		sliders = sliders.filter(Slider.DivId != notDivId)
	sliders = sliders\
		.options(joinedload(Slider.Sl_image))\
		.all()
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
		.options(joinedload(Slider.Sl_image))\
		.first()
	data = []
	status_code = 404
	if slider:
		try:
			data = slider.to_json_api()
			data["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if sl_image.GCRecord == None]
			status_code = 200
		except Exception as ex:
			print(f"{datetime.now()} | Slider Api Exception: {ex}")

	res = {
		"status": 1,
		"message": "Slider",
		"data": data,
		"total": 1
	}
	response = make_response(jsonify(res),status_code)
	return response