from flask import make_response, jsonify

def respond_with_json(data, message, status_code = 200):
	res = {
		"data": data,
		"total": len(data),
		"status": 1 if len(data) > 0 else 0,
		"message": message,
	}
	return make_response(jsonify(res)), status_code