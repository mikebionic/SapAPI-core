from flask import make_response, jsonify, render_template, request, abort
from . import bp
from main_pack.config import Config
from flask_wtf.csrf import CSRFError
from main_pack.commerce.commerce.utils import UiCategoriesList

# !!! Prepare template error on admin page or handle on client app


@bp.app_errorhandler(400)
def bad_request(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Bad request"}), 400)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",**UiCategoriesList()), 500


@bp.app_errorhandler(401)
def unauthorized(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Forbidden"}), 401)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",**UiCategoriesList()), 500


@bp.app_errorhandler(403)
def forbidden(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Forbidden"}), 403)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/403.html",**UiCategoriesList()), 403


@bp.app_errorhandler(404)
def not_found(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Not found"}), 404)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/404.html",**UiCategoriesList()), 404


@bp.app_errorhandler(405)
def method_not_found(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Method not found"}), 405)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/405.html",**UiCategoriesList()), 405


@bp.app_errorhandler(410)
def gone(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Gone"}), 410)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/410.html",**UiCategoriesList()), 410


@bp.app_errorhandler(500)
def internal_server_error(error):
	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify({"error": "Server error"}), 500)
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",**UiCategoriesList()), 500


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(e):
	return {"status": "CSRFError","reason":e.description}, 400