from flask import render_template
from main_pack.commerce.errors import bp

@bp.app_errorhandler(404)
def page_not_found(error):
	return render_template("commerce/main/errors/404.html"), 404

@bp.app_errorhandler(403)
def forbidden(error):
	return render_template("commerce/main/errors/403.html"), 403

# @bp.app_errorhandler(405)
# def method_not_found(error):
# 	return render_template("commerce/errors/405.html"), 405

# @bp.app_errorhandler(410)
# def gone(error):
# 	return render_template("commerce/errors/410.html"), 410

# @bp.app_errorhandler(500)
# def internal_server_error(error):
# 	return render_template("commerce/errors/500.html"), 500