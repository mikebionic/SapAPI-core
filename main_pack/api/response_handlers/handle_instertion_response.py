from flask import make_response, jsonify
from main_pack.base.apiMethods import checkApiResponseStatus

def handle_instertion_response(data, fails, message, status_code = 200):
	status = checkApiResponseStatus(data, fails)

	res = {
		"data": data,
		"fails": fails,
		"success_total": len(data),
		"fail_total": len(fails)
	}

	for e in status:
		res[e] = status[e]

	status_code = 201 if len(data) > 0 else 200
	return make_response(jsonify(res), status_code)