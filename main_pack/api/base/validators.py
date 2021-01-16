from flask import request, make_response, jsonify
from functools import wraps


def request_is_json(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		print(request.method != 'GET')
		print(request.method)
		if (request.method != 'GET' and not request.json):
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			return make_response(jsonify(res), 400)

		return f(*args,**kwargs)

	return decorated