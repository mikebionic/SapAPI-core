from flask import make_response, jsonify

def respond_with_json(data, message, status_code = 200):
	status = checkApiResponseStatus(data, failed_data)

	res = {
		"data": data,
		"fails": failed_data,
		"success_total": len(data),
		"fail_total": len(failed_data)
	}

	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	response = make_response(jsonify(res), status_code)