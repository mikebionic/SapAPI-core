from flask import jsonify,request,make_response
import uuid

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.models.users.models import Device
from .utils import sap_key_required


@api.route("/devices/register/",methods=["POST"])
# @sap_key_required
def register_device():
	if request.method == 'POST':
		# if not request.json:
		# 	res = {
		# 		"status": 0,
		# 		"message": "Error. Not a JSON data."
		# 	}
		# 	response = make_response(jsonify(res),400)
			
		# else:
		print("request handling")
		try:

			req = request.get_json()
			
			print("printing sap side")
			print(req)
			
			filtering = {
				"GCRecord": None,
				"DevUniqueId": req["DevUniqueId"]
			}

			thisDevice = Device.query.filter_by(**filtering).first()

			data = {}
			if thisDevice:
				data = thisDevice.to_json_api()

			else:
				req["DevGuid"] = uuid.uuid4()
				thisDevice = Device(**req)
				db.session.add(thisDevice)
				db.session.commit()
				print("printing sap side")
				print(thisDevice.to_json_api())
				data = thisDevice.to_json_api()

			res = {
				"status": 1 if data else 0,
				"data": data,
				"message": "Device registration",
				"total": 1 if data else 0
			}
			print('sap response')
			print(res)
			response = make_response(jsonify(res),200)
		except Exception as ex:
			print(ex)
		return response