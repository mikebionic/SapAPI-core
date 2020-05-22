from flask import render_template
from main_pack.commerce.errors import bp

from main_pack.commerce.commerce.utils import commonUsedData

@bp.app_errorhandler(404)
def page_not_found(error):
	commonData = commonUsedData()
	return render_template("commerce/main/errors/404.html",**commonData), 404

@bp.app_errorhandler(403)
def forbidden(error):
	commonData = commonUsedData()
	return render_template("commerce/main/errors/403.html",**commonData), 403

@bp.app_errorhandler(405)
def method_not_found(error):
	commonData = commonUsedData()
	return render_template("commerce/main/errors/405.html",**commonData), 405

@bp.app_errorhandler(410)
def gone(error):
	commonData = commonUsedData()
	return render_template("commerce/main/errors/410.html",**commonData), 410

@bp.app_errorhandler(500)
def internal_server_error(error):
	commonData = commonUsedData()
	return render_template("commerce/main/errors/500.html",**commonData), 500