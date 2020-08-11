from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api

from main_pack.models.base.models import Company,Sl_image,Slider
from sqlalchemy import or_, and_
# from main_pack.api.auth.api_login import sha_required

@api.route("/tbl-dk-sliders/")
def api_sliders():
	company = Company.query.get(1)
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