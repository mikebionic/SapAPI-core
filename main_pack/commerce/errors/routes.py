from flask import render_template
from main_pack.commerce.errors import bp
from main_pack.config import Config
from flask_wtf.csrf import CSRFError
from main_pack.commerce.commerce.utils import UiCategoriesList

@bp.app_errorhandler(404)
def page_not_found(error):
	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/404.html",**categoryData), 404

@bp.app_errorhandler(403)
def forbidden(error):
	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/403.html",**categoryData), 403

@bp.app_errorhandler(405)
def method_not_found(error):
	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/405.html",**categoryData), 405

@bp.app_errorhandler(410)
def gone(error):
	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/410.html",**categoryData), 410

@bp.app_errorhandler(500)
def internal_server_error(error):
	categoryData = UiCategoriesList()
	return render_template(f"{Config.COMMERCE_TEMPLATES_FOLDER_PATH}/errors/500.html",**categoryData), 500

@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
	return {'status':'CSRFError','reason':e.description}, 400