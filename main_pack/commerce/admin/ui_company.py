from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCompanyInfoDict
from main_pack.models.base.models import Company

@bp.route("/admin/ui_company/", methods=['POST'])
@login_required
@ui_admin_required
def ui_company():
	company = Company.query.get(1)
	baseTemplate = {
		'company':company,
		}
	if request.method == 'POST':
		try:
			req = request.get_json()
			companyInfo = addCompanyInfoDict(req)
			company.update(**companyInfo)
			db.session.commit()
			response = jsonify({
				"companyId": company.CId,
				"status": "updated",
				"responseText": gettext('Company')+' '+gettext('successfully updated!'),
				})
		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": "error",
				"responseText": gettext('Unknown error!'),
				})

	return response