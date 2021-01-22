# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

from main_pack.api.commerce import api
from main_pack.models.base.models import Company, Sl_image, Slider


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

	# !!! TODO: this situation is discussed and we return [{}] instead of {} even on single response
	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All view sliders",
		"data": data,
		"total": len(data)
	}

	response = make_response(jsonify(res), 200)

	return response


@api.route("/tbl-dk-sliders/<SlName>/")
def api_slider_info(SlName):

	slider = Slider.query\
		.filter_by(GCRecord = None, SlName = SlName)\
		.options(joinedload(Slider.Sl_image))\
		.first()

	data = {}

	if slider:
		try:
			data = slider.to_json_api()
			data["Sl_images"] = [sl_image.to_json_api() for sl_image in slider.Sl_image if not sl_image.GCRecord]

		except Exception as ex:
			print(f"{datetime.now()} | Slider Api Exception: {ex}")

	res = {
		"status": 1 if data else 0,
		"message": "Slider",
		"data": data,
		"total": 1 if data else 0
	}
	status_code = 200 if data else 404
	response = make_response(jsonify(res), status_code)
	return response