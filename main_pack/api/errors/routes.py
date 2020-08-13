from main_pack.api.errors import api
from flask import make_response, jsonify

@api.errorhandler(404)
def not_found(error):
	return make_response(jsonify({"error": "Not found"}), 404)

@api.errorhandler(401)
def unauthorized(error):
	return make_response(jsonify({"error": "Forbidden"}), 401)

@api.errorhandler(403)
def forbidden(error):
	return make_response(jsonify({"error": "Forbidden"}), 403)

@api.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({"error": "Bad request"}), 400)

@api.errorhandler(405)
def method_not_found(error):
	return make_response(jsonify({"error": "Method not found"}), 405)

@api.errorhandler(410)
def gone(error):
	return make_response(jsonify({"error": "Gone"}), 410)

@api.errorhandler(500)
def server_error(error):
	return make_response(jsonify({"error": "Server error"}), 500)
