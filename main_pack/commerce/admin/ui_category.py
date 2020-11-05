from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext
from main_pack.config import Config

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCategoryDict
from main_pack.models.commerce.models import Res_category


@bp.route('/ui/category_table/', methods=['POST','DELETE'])
@login_required
@ui_admin_required()
def ui_category_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			category = addCategoryDict(req)
			categoryId = req.get('categoryId')

			if (categoryId == '' or categoryId == None):
				newCategory = Res_category(**category)
				db.session.add(newCategory)
				db.session.commit()
				response = jsonify({
					"categoryId": newCategory.ResCatId,
					"status": "created",
					"responseText": gettext('Category')+' '+gettext('successfully saved'),
					"htmlData":  render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/categoryAppend.html",category=newCategory)
					})
			else:
				thisCategory = Res_category.query.get(categoryId)
				thisCategory.update(**category)
				db.session.commit()
				response = jsonify({
					"status": "updated",
					"responseText": gettext('Category')+' '+gettext('successfully updated'),
					})			
		elif request.method == 'DELETE': 
			req = request.get_json()
			categoryId = req.get('categoryId')
			thisCategory = Res_category.query.get(categoryId)

			# checking for presense of resources in this category
			category_resources = [resource for resource in thisCategory.Resource if resource.GCRecord == None]
			if category_resources:
				response = jsonify({
					"status": "error",
					"responseText": gettext('Error')+', '+gettext('category has resources, delete related resources first and try again.'),
					})
				return response

			thisCategory.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": "deleted",
				"responseText": gettext('Category')+' '+gettext('successfully deleted'),
				})
	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": "error",
			"responseText": gettext('Unknown error!'),
			})
	return response
