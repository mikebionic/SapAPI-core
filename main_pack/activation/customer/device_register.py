from flask import jsonify, request, make_response
from datetime import datetime
import uuid

from . import api
from .make_register_request import make_register_request
from .add_device_to_db import add_device_to_db

from main_pack.config import Config
from main_pack.api.base.validators import request_is_json
from main_pack.models import Device


@api.route("/devices/register/",methods=["POST"])
@request_is_json(request)
def register_device():
	req = request.get_json()

	req["DevName"] = str(datetime.now().timestamp())
	req["DevGuid"] = str(uuid.uuid4())

	data = {}

	if not Config.USE_SERVERLESS_ACTIVATION:
		registered_req = make_register_request(req)
		if registered_req:
			req = registered_req

	filtering = {
		"GCRecord": None,
		"DevUniqueId": req["DevUniqueId"]
	}
	thisDevice = Device.query.filter_by(**filtering).first()

	data = add_device_to_db(req, thisDevice)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Device registration",
		"total": 1 if data else 0
	}
	response = make_response(jsonify(res), 200)

	return response