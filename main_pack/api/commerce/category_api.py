# -*- coding: utf-8 -*-
from flask import render_template,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

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
			"status":1,
			"data":category.to_json_api()
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		category = Res_category.query.get(id)
		updateCategory = addCategoryDict(req)
		category.update(**category)
		res = {
			"status":1,
			"message":"Category updated",
			"data":category.to_json_api(),
		}
		response = make_response(jsonify(res),200)
	return response


@api.route("/categories/",methods=['GET','POST','PUT'])
def api_categories():
	if request.method == 'GET':
		categories = Res_category.query.all()
		res = {
			"status":1,
			"message":"All categories",
			"data":[category.to_json_api() for category in categories],
			"total":len(categories)
		}
		response = make_response(jsonify(res),200)
		

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status":0,
				"message":"Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			categories = []
			failed_categories = [] 
			for category in req:
				# # fix this
				# if not category['ResCatName']:
				# 	res = {
				# 		"status": 0,
				# 		"message": "Error. ResCatName is None."
				# 	}

				category = addCategoryDict(category)
				try:
					newCategory = Res_category(**category)
					db.session.add(newCategory)
					db.session.commit()
					categories.append(category)
				except:
					failed_categories.append(category)

			status = checkApiResponseStatus(categories,failed_categories)
			res = {
				"status":status,
				"message":"Categories added",
				"data":categories,
				"fails":failed_categories,
				"success_total":len(categories),
				"fail_total":len(failed_categories)
			}

			response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
		else:
			req = request.get_json()
			categories = []
			failed_categories = [] 
			for category in req:
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
			
			status = checkApiResponseStatus(categories,failed_categories)
			res = {
				"status":status,
				"message":"Categories updated",
				"data":categories,
				"fails":failed_categories,
				"success_total":len(categories),
				"fail_total":len(failed_categories)
			}

			response = make_response(jsonify(res),200)

	elif request.method == 'DELETE':
		if not request.json:
			res = {
				"status":0,
				"message":"Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			categories = []
			failed_categories = []
			for category in req:
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
			
			status = checkApiResponseStatus(categories,failed_categories)
			res = {
				"status":status,
				"message":"Categories deleted",
				"data":categories,
				"fails":failed_categories,
				"success_total":len(categories),
				"fail_total":len(failed_categories)
			}

			response = make_response(jsonify(res),200)
	
	return response

@api.route("/paginated_categories/",methods=['GET'])
def api_paginated_categories():
	page = request.args.get('page',1,type=int)
	pagination = Res_category.query\
	.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None)\
	.order_by(Res_category.CreatedDate.desc()).paginate(
		page,per_page=current_app.config['API_OBJECTS_PER_PAGE'],
		error_out=False
		)
	categories = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('commerce_api.api_paginated_categories',page=page-1)
	next = None
	if pagination.has_next:
		next = url_for('commerce_api.api_paginated_categories',page=page+1)
	
	res = {
		"status":1,
		"message":"Categories",
		"data":[category.to_json_api() for category in categories],
		"total":len(categories),
		'prev_url':prev,
		'next_url':next,
		'pages_total':pagination.total
	}
	
	return jsonify(res)