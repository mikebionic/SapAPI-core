from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCategoryDict
from main_pack.models.base.models import Resource_category

@bp.route("/admin/category/", methods=['GET','POST'])
def ui_category_commerce():
	categories = Resource_category.query.all()
	baseTemplate = {
		'categories':categories,
		}
	if request.method == "POST":
		try:
			req = request.get_json()
			category = addCategoryDict(req)
			newCategory = Resource_category(**category)
			db.session.add(newCategory)
			db.session.commit()
			if (newCategory.ResOwnerCatId == '' or newCategory.ResOwnerCatId == None):
				child_status = "category"
			else:
				parent = Resource_category.query.filter_by(ResOwnerCatId=newCategory.ResOwnerCatId).first()
				if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None):
					child_status = "category_child"
				else:
					child_status = "subcategory_child"
			response = jsonify({
				'catId':newCategory.RegCatId,
				'status':'created',
				'child_status':child_status,
				'responseText':gettext('Category')+' '+gettext('successfully saved!'),
				'data':render_template('commerce/admin/appendingCategory.html',child_status=child_status,category=newCategory)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	return response