# -*- coding: utf-8 -*-
from flask import render_template,jsonify,request,abort,make_response
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Res_category
from main_pack.api.commerce.utils import addCategoryDict
from main_pack import db
from flask import current_app

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
		res = {
			"status": "success",
			"message": "All categories",
			"data":{
				"categories":[category.to_json_api() for category in categories],
				"total":len(categories)
			}
		}
		response = make_response(jsonify(res),200)
		

	elif request.method == 'POST':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			categories = []
			failed_categories = [] 
			for category in req['categories']:
				if not category['ResCatName']:
					abort(400)
				category = addCategoryDict(category)
				try:
					newCategory = Res_category(**category)
					db.session.add(newCategory)
					db.session.commit()
					categories.append(category)
				except:
					failed_categories.append(category)

			res = {
				"status": "success",
				"message": "Categories added",
				"data":{
					"categories":categories,
					"total":len(categories)
				}
			}
			if len(failed_categories)>0:
				res["data"]["fails"] = failed_categories

			response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			categories = []
			failed_categories = [] 
			for category in req['categories']:
				category = addCategoryDict(category)
				try:
					ResCatId = category['ResCatId']
					thisCategory = Res_category.query.get(ResCatId)
					thisCategory.update(**category)
					thisCategory.modifiedInfo(UId=1)
					db.session.commit()

					categories.append(category)
				except:
					failed_categories.append(category)
			
			res = {
				"status": "success",
				"message": "Categories updated",
				"data":{
					"categories":categories,
					"total":len(categories)
				}
			}
			if len(failed_categories)>0:
				res["data"]["fails"] = failed_categories

			response = make_response(jsonify(res),200)

	elif request.method == 'DELETE':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			categories = []
			failed_categories = []
			for category in req['categories']:
				category = addCategoryDict(category)
				try:
					ResCatId = category['ResCatId']
					thisCategory = Res_category.query.get(ResCatId)
					thisCategory.GCRecord = int(datetime.now().strftime("%H"))
					thisCategory.modifiedInfo(UId=1)
					db.session.commit()
					categories.append(category)
				except:
					failed_categories.append(category)
			
			res = {
				"status": "success",
				"message": "Categories deleted",
				"data":{
					"categories":categories,
					"total":len(categories)
				}
			}
			if len(failed_categories)>0:
				res["data"]["fails"] = failed_categories

			response = make_response(jsonify(res),200)
	
	return response

@api.route("/paginated_categories/",methods=['GET'])
def api_paginated_categories():
	page = request.args.get('page',1,type=int)
	pagination = Resource.query\
	.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
	.order_by(Resource.CreatedDate.desc()).paginate(
		page,per_page=current_app.config['API_OBJECTS_PER_PAGE'],
		error_out=False
		)
	resources = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('commerce_api.api_paginate_resources',page=page-1)
	next = None
	if pagination.has_next:
		next = url_for('commerce_api.api_paginate_resources',page=page+1)
	
	res = {
		"status":"success",
		"message":"Resources",
		"data":{
			"resources":[resource.to_json_api() for resource in resources],
			"total":len(resources)
		},
		'prev_url':prev,
		'next_url':next,
		'pages_total':pagination.total
	}
	
	return jsonify(res)