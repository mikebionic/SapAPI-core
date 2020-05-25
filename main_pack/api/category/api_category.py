from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from main_pack.api.category import api

# from main_pack import db,babel,gettext,lazy_gettext
# from main_pack.commerce.admin import api

from main_pack.models.commerce.models import Res_category
from main_pack.api.category.utils import addCategoryDict



@api.route("/categories/<int:id>/",methods=['GET','PUT'])
def api_category(id):
	if request.method == 'GET':
		category = Res_category.query.get(id)
		response = jsonify({'category':category.to_json_api()})
		res = {
			"status": "success",
			"data":{
				"category":category.to_json_api(),
			}
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		category = Res_category.query.get(id)
		updateCategory = addCategoryDict(req)
		category.update(**category)
		res = {
			"status": "success",
			"message": "Category updated",
			"data":{
				"category":category.to_json_api(),
			}
		}
		response = make_response(jsonify(res),200)
	return response

@api.route("/categories/",methods=['GET','POST','PUT'])
def api_categories():
	if request.method == 'GET':
		categories = Res_category.query.all()
		response = jsonify({'categories':[category.to_json_api() for category in categories]})
		return response
	elif request.method == 'POST':
		if not request.json or not 'ResCatName' in request.json:
			abort(400)
		else:
			req = request.get_json()
			category = addCategoryDict(req)
			newCategory = Res_category(**category)
			db.session.add(newCategory)
			db.session.commit()
			res = {
				"status": "success",
				"message": "Category added",
				"data":{
					"category":newCategory.to_json_api(),
				}
			}
			response = make_response(jsonify(res),200)
			return response

	elif request.method == 'PUT':
		if not request.json or not 'ResCatId' in request.json:
			abort(400)
		else:
			req = request.get_json()
			try:
				ResCatId = req.get('ResCatId')
				updateCategory = addCategoryDict(req)
				category = Res_category.query.get(ResCatId)
				category.update(**updateCategory)
				category.modifiedInfo(UId=1)
				db.session.commit()
				res = {
					"status": "success",
					"message": "Category updated",
					"data":{
						"category":category.to_json_api(),
					}
				}
				response = make_response(jsonify(res),200)
				return response
			except:
				res = {
					"status": "error",
					"message": "Update failed",
				}
				response = make_response(jsonify(res),400)
				return response

	elif request.method == 'DELETE':
		if not request.json or not 'ResCatId' in request.json:
			abort(400)
		else:
			req = request.get_json()
			try:
				ResCatId = req.get('ResCatId')
				category = Res_category.query.get_or_404(ResCatId)
				category.GCRecord = int(datetime.now().strftime("%H"))
				category.modifiedInfo(UId=1)
				db.session.commit()
				res = {
					"status": "success",
					"message": "Category deleted",
				}
				response = make_response(jsonify(res),400)
				
			except:
				res = {
					"status": "error",
					"message": "Deletion failed, no change",
				}
				response = make_response(jsonify(res),400)
			return response


# @api.route('/api/employees/',methods=['DELETE'])
# @token_required
# def delete_employee(current_user):


#####
# @api.route("/category/", methods=['POST','DELETE'])
# def ui_category():
# 	categories = Res_category.query.all()
# 	baseTemplate = {
# 		'categories':categories,
# 		}
# 	if request.method == "POST":
# 		try:
# 			req = request.get_json()
# 			category = addCategoryDict(req)
# 			newCategory = Res_category(**category)
# 			db.session.add(newCategory)
# 			db.session.commit()
# 			if (newCategory.ResOwnerCatId == '' or newCategory.ResOwnerCatId == None or newCategory.ResOwnerCatId == 0):
# 				child_status = "category"
# 			else:
# 				parent = Res_category.query.filter_by(ResCatId=newCategory.ResOwnerCatId).first()
# 				if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
# 					child_status = "subcategory"
# 				else:
# 					child_status = "subcategory_child"
# 			response = jsonify({
# 				'catId':newCategory.ResCatId,
# 				'status':'created',
# 				'child_status':child_status,
# 				'responseText':gettext('Category')+' '+gettext('successfully saved!'),
# 				'htmlData':render_template('commerce/admin/appendCategory.html',child_status=child_status,category=newCategory)
# 				})
# 		except:
# 			response = jsonify({
# 				'status':'error',
# 				'responseText':gettext('Unknown error!'),
# 				})

# 	elif request.method == "DELETE":
# 		try:
# 			req = request.get_json()
# 			catId = req.get('catId')
# 			thisCategory = Res_category.query.get(catId)
# 			thisCategory.GCRecord = 1
# 			db.session.commit()
# 			response = {
# 				'status':'deleted',
# 				'responseText':thisCategory.ResCatName+' '+gettext('successfully deleted'),
# 			}
# 		except:
# 			response = jsonify({
# 				'status':'error',
# 				'responseText':gettext('Unknown error!'),
# 				})

# 	return response
