
from flask import make_response, jsonify, request

from main_pack.api.auth import api

@api.route('/sms-register/',methods=['POST'])
def sms_register():
	req = request.get_json()
	print("headers: ", request.headers)
	print("phone: ", req.get('phone_number'))
	print("message: ", req.get('message_text'))
	return make_response(jsonify(req))