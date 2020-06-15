from flask import render_template
from main_pack.commerce.errors import bp

from main_pack.commerce.commerce.utils import UiCategoriesList

@bp.app_errorhandler(404)
def page_not_found(error):
	categoryData = UiCategoriesList()
	return render_template("commerce/main/errors/404.html",**categoryData), 404

@bp.app_errorhandler(403)
def forbidden(error):
	categoryData = UiCategoriesList()
	return render_template("commerce/main/errors/403.html",**categoryData), 403

@bp.app_errorhandler(405)
def method_not_found(error):
	categoryData = UiCategoriesList()
	return render_template("commerce/main/errors/405.html",**categoryData), 405

@bp.app_errorhandler(410)
def gone(error):
	categoryData = UiCategoriesList()
	return render_template("commerce/main/errors/410.html",**categoryData), 410

@bp.app_errorhandler(500)
def internal_server_error(error):
	categoryData = UiCategoriesList()
	return render_template("commerce/main/errors/500.html",**categoryData), 500