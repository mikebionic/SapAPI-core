from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addResourceDict
from main_pack import db
from flask import current_app

@api.route("/resources/<int:id>/",methods=['GET','PUT'])
def api_resource(id):
	if request.method == 'GET':
		resource = Resource.query.get(id)
		response = jsonify({'resource':resource.to_json_api()})
		res = {
			"status":"success",
			"data":{
				"resource":resource.to_json_api(),
			}
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		resource = Resource.query.get(id)
		# miguelGrinberg's method
		# resource.from_json(request.json)
		updateResource = addResourceDict(req)
		resource.update(**resource)
		res = {
			"status":"success",
			"message":"resource updated",
			"data":{
				"resource":resource.to_json_api(),
			}
		}
		response = make_response(jsonify(res),200)
	return response

@api.route("/resources/",methods=['GET','POST','PUT'])
def api_resources():
	if request.method == 'GET':
		resources = Resource.query.all()
		res = {
			"status":"success",
			"message":"All resources",
			"data":{
				"resources":[resource.to_json_api() for resource in resources],
				"total":len(resources)
			}
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			resources = []
			failed_resources = [] 
			for resource in req['resources']:
				resource = addResourceDict(resource)
				try:
					newResource = Resource(**resource)
					db.session.add(newResource)
					db.session.commit()
					resources.append(resource)
				except:
					failed_resources.append(category)

			res = {
				"status": "success",
				"message":"Resources added",
				"data":{
					"resources":resources,
					"total":len(resources)
				}
			}
			if len(failed_resources)>0:
				res["data"]["fails"] = failed_resources

			response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			resources = []
			failed_resources = [] 
			for resource in req['resources']:
				resource = addResourceDict(resource)
				try:
					ResId = resource['ResId']
					thisResource = Resource.query.get(ResId)
					thisResource.update(**resource)
					thisResource.modifiedInfo(UId=1)
					db.session.commit()
					resources.append(resource)
				except:
					failed_resources.append(resource)

			res = {
				"status":"success",
				"message":"Resources updated",
				"data":{
					"resources":resources,
					"total":len(resources)
				}
			}
			if len(failed_resources)>0:
				res["data"]["fails"] = failed_resources
			
			response = make_response(jsonify(res),200)

	elif request.method == 'DELETE':
		if not request.json or not 'ResId' in request.json:
			abort(400)
		else:
			req = request.get_json()
			resources = []
			failed_resources = [] 
			for resource in req['resources']:
				resource = addResourceDict(resource)
				try:
					ResId = resource['ResId']
					thisResource = Resource.query.get(ResId)
					thisResource.GCRecord = int(datetime.now().strftime("%H"))
					thisResource.modifiedInfo(UId=1)
					db.session.commit()
					resources.append(resource)
				except:
					failed_resources.append(resource)

			res = {
				"status":"success",
				"message":"Resources deleted",
				"data":{
					"resources":resources,
					"total":len(resources)
				}
			}
			if len(failed_resources)>0:
				res["data"]["fails"] = failed_resources
			
			response = make_response(jsonify(res),200)
	
	return response


@api.route("/paginated_resources/",methods=['GET'])
def api_paginated_resources():
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
		prev = url_for('commerce_api.api_paginated_resources',page=page-1)
	next = None
	if pagination.has_next:
		next = url_for('commerce_api.api_paginated_resources',page=page+1)
	
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

@api.route("/just_resources/",methods=['GET'])
def api_just_resources():
	if request.method == 'GET':
		resources = Resource.query.all()
		res = [
			resource.to_json_api() for resource in resources
		]
		response = make_response(jsonify(res),200)

		return response