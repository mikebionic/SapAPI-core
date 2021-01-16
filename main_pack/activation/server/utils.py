from flask import request
from functools import wraps

from main_pack.config import Config


def sap_key_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({"message": "Token is missing!"}), 401
		
		if token != Config.SAP_SERVICE_KEY:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(*args,**kwargs)

	return decorated