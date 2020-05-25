from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from main_pack.api.category import api

# from main_pack import db,babel,gettext,lazy_gettext
# from main_pack.commerce.admin import api
# from main_pack.commerce.admin.utils import addCategoryDict

from main_pack.models.commerce.models import Res_category


@api.route("/category/",methods=['GET','DELETE'])
def api_category():
	if request.method == 'GET':
		categories = Res_category.query.all()
		
		response = jsonify({'categories':[category.to_json_api() for category in categories]})
		
		return response

	else:
		return 405


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
