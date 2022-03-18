from flask import make_response, jsonify

def handle_default_response(data, message="", status_code=None, headers=None, total=None):
	res = {
		"data": data,
		"status": 1 if data else 0,
		"total": total if total else len(data),
		"message": message if message else "Api response"
	}

	if not status_code:
		status_code = 200 if data else 404

	return make_response(jsonify(res)), status_code, headers