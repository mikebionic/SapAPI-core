from flask import jsonify,request,make_response
import requests

from . import api
from main_pack import db
from main_pack.config import Config
from main_pack.models.users.models import Device


@api.route("/devices/register/",methods=["POST"])
def register_device():
	if request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()

			filtering = {
				"GCRecord": None,
				"DevUniqueId": req["DevUniqueId"]
			}

			thisDevice = Device.query.filter_by(**filtering).first()

			data = {}
			if thisDevice:
				print("customer, found device")
				data = thisDevice.to_json_api()

			else:
				print("customer, starting request")
				r = requests.post(
					Config.SAP_SERVICE_URL,
					data = req,
					headers = {
						'Content-type': 'application/json',
						'x-access-token': Config.SAP_SERVICE_KEY})

				print(r.status_code)
				print(r.text())
				try:
					print(r.json())
					server_response = r.json()
				except:
					print("errror json")

				if (r.status_code != 500):
					if server_response["status"] != 0:
						data = server_response["data"]
						print("customer, server response")
						print(data)
						try:
							thisDevice = Device(**data)
							db.session.add(thisDevice)
							db.session.commit()
						except Exception as ex:
							print(ex)

			res = {
				"status": 1 if data else 0,
				"data": data,
				"message": "Device registration",
				"total": 1 if data else 0
			}
			response = make_response(jsonify(res),200)

		return response
# {
# 	"DevUniqueId": "e4d788879fbe6635",
# 	"DevName": "2021-01-14 23:44:26.778464",
# 	"DevDesc": "",
# 	"AddInf1": "",
# 	"AddInf2": "",
# 	"AddInf3": "",
# 	"AddInf4": "",
# 	"AddInf5": "",
# 	"AddInf6": "id=QP1A.190711.020,androidId=e4d788879fbe6635,baseOS=,release=10,brand=samsung,device=a7y18lte,display=QP1A.190711.020.A750FXXU5CTK1,manufacturer=samsung,model=SM-A750F,isPhysicalDevice=true"
# }