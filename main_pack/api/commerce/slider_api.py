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
	SlId = request.args.get("id",None,type=int)
	SlName = request.args.get("name",None,type=str)

	filtering = {"GCRecord": None}

	if DivId:
		filtering["DivId"] = DivId
	if SlId:
		filtering["SlId"] = SlId
	if SlName:
		filtering["SlName"] = SlName

	sliders = Slider.query.filter_by(**filtering)

	if notDivId:
		sliders = sliders.filter(Slider.DivId != notDivId)

	sliders = sliders\
		.options(joinedload(Slider.Sl_image))\
		.all()

	data = []
	for slider in sliders:
		slider_info = slider.to_json_api()
		slider_info["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if not sl_image.GCRecord]
		data.append(slider_info)

	status_code = 200 if len(data) > 0 else 404

	# !!! TODO: Discuss this situation of returning a single {} inside data or [{}] as it is by default
	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All view sliders",
		"data": data[0] if len(data) == 1 else data,
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
			data["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if not sl_image.GCRecord]
			status_code = 200

		except Exception as ex:
			print(f"{datetime.now()} | Slider Api Exception: {ex}")

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Slider",
		"data": data,
		"total": 1
	}
	response = make_response(jsonify(res),status_code)
	return response