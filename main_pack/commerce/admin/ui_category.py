from flask import render_template,url_for,jsonify,json,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCategoryDict,addEditCategoryDict
from main_pack.models.commerce.models import Res_category

@bp.route("/admin/category/", methods=['POST','DELETE'])
def ui_category():
	try:
		if request.method == 'POST':
			req = request.get_json()
			category = addCategoryDict(req)
			categoryId = req.get('categoryId')
			editCategoryId = req.get('editCategoryId')

			if (editCategoryId == '' or editCategoryId == None):
				print('committing')
				newCategory = Res_category(**category)
				db.session.add(newCategory)
				db.session.commit()
				if (newCategory.ResOwnerCatId == '' or newCategory.ResOwnerCatId == None or newCategory.ResOwnerCatId == 0):
					child_status = "category"
				else:
					parent = Res_category.query.filter_by(ResCatId=newCategory.ResOwnerCatId).first()
					if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
						child_status = "subcategory"
					else:
						child_status = "subcategory_child"
				response = jsonify({
					'catId':newCategory.ResCatId,
					'status':'created',
					'child_status':child_status,
					'responseText':gettext('Category')+' '+gettext('successfully saved!'),
					'htmlData':render_template('commerce/admin/appendCategory.html',child_status=child_status,category=newCategory)
					})
			else:
				category = addEditCategoryDict(req)
				print('updating')
				thisCategory = Res_category.query.get(editCategoryId)
				thisCategory.update(**category)
				db.session.commit()
				response = jsonify({
					'status':'updated',
					'responseText':thisCategory.ResCatName+' '+gettext('successfully updated'),
					})

		elif request.method == "DELETE":
			req = request.get_json()
			categoryId = req.get('categoryId')
			thisCategory = Res_category.query.get(categoryId)
			thisCategory.GCRecord = 1
			db.session.commit()
			response = {
				'status':'deleted',
				'responseText':thisCategory.ResCatName+' '+gettext('successfully deleted'),
			}
	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})
	return response

@bp.route('/ui/category_table/', methods=['POST','DELETE'])
def ui_category_table():
	try:
		if request.method == 'POST':
			req = request.get_json()
			category = addCategoryDict(req)
			categoryId = req.get('categoryId')

			if (categoryId == '' or categoryId == None):
				print('committing')
				newCategory = Res_category(**category)
				db.session.add(newCategory)
				db.session.commit()
				response = jsonify({
					'categoryId':newCategory.ResCatId,
					'status':'created',
					'responseText':gettext('Category')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/categoryAppend.html',category=newCategory)
					})
			else:
				print('updating')
				thisCategory = Res_category.query.get(categoryId)
				thisCategory.update(**category)
				db.session.commit()
				response = jsonify({
					'status':'updated',
					'responseText':gettext('Category')+' '+gettext('successfully updated'),
					})			
		elif request.method == 'DELETE':
			req = request.get_json()
			print(req)
			categoryId = req.get('categoryId')
			thisCategory = Res_category.query.get(categoryId)
			thisCategory.GCRecord = 1
			db.session.commit()
			response = jsonify({
				'status':'deleted',
				'responseText':gettext('Category')+' '+gettext('successfully deleted'),
				})
	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})
	return response
