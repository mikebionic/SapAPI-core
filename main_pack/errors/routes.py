from flask import (
	make_response,
	jsonify,
	render_template,
	request,
	redirect,
	url_for,
)
from flask_wtf.csrf import CSRFError

from . import bp
from main_pack.config import Config
from main_pack.commerce.commerce.utils import UiCategoriesList

# !!! Prepare template error on admin page or handle on client app

@bp.app_errorhandler(400)
def bad_request(error):
	res = {
		"error": "Bad request",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 400)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",
		title = res["error"],
		**UiCategoriesList()), 500


@bp.app_errorhandler(401)
def unauthorized(error):
	res = {
		"error": "Unauthorized",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 401)

	return redirect(url_for('commerce_auth.login'))


@bp.app_errorhandler(403)
def forbidden(error):
	res = {
		"error": "Forbidden",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 403)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/403.html",
		title = res["error"],
		**UiCategoriesList()), 403


@bp.app_errorhandler(404)
def not_found(error):
	res = {
		"error": "Not found",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 404)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/404.html",
		title = res["error"],
		**UiCategoriesList()), 404


@bp.app_errorhandler(405)
def method_not_found(error):
	res = {
		"error": "Method not found",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 405)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/405.html",
		title = res["error"],
		**UiCategoriesList()), 405


@bp.app_errorhandler(410)
def gone(error):
	res = {
		"error": "Gone",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 410)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/410.html",
		title = res["error"],
		**UiCategoriesList()), 410


@bp.app_errorhandler(500)
def internal_server_error(error):
	res = {
		"error": "Forbidden",
		"message": str(error)
	}

	if (request.path.startswith(Config.API_URL_PREFIX) or Config.API_AND_ADMIN_ONLY):
		return make_response(jsonify(res), 500)

	return render_template(
		f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",
		title = res["error"],
		**UiCategoriesList()), 500


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(e):
	return {"status": "CSRFError","reason":e.description}, 400