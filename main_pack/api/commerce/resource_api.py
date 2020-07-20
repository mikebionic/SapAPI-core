from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Res_category
from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addResourceDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required

@api.route("/tbl-dk-resources/<int:ResId>/",methods=['GET'])
def api_resource(ResId):
	if request.method == 'GET':
		resource = Resource.query.get(ResId)
		response = jsonify({'resource':resource.to_json_api()})
		res = {
			"status":1,
			"data":resource.to_json_api()
		}
		response = make_response(jsonify(res),200)

	# elif request.method == 'PUT':
	# 	resource = Resource.query.get(ResId)
	# 	# miguelGrinberg's method
	# 	# resource.from_json(request.json)
	# 	updateResource = addResourceDict(req)
	# 	resource.update(**resource)
	# 	res = {
	# 		"status":1,
	# 		"message":"Resource updated",
	# 		"data":resource.to_json_api()
	# 	}
	# 	response = make_response(jsonify(res),200)
	return response

@api.route("/tbl-dk-resources/",methods=['GET','POST'])
@sha_required
def api_resources():
	if request.method == 'GET':
		resources = Resource.query\
			.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
		res = {
			"status":1,
			"message":"All resources",
			"data":[resource.to_json_api() for resource in resources],
			"total":len(resources)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			resources = []
			failed_resources = [] 
			for resource in req:
				resource = addResourceDict(resource)

				# special syncronizer method
				group = resource['AddInf2']
				print(group)
				if group:
					category = Res_category.query.filter_by(ResCatName=group).first()
					if not category:
						category = Res_category(ResCatName=group)
						db.session.add(category)
						db.session.commit()
						resource['ResCatId']=category.ResCatId
						print("resCat added, it's id: "+str(category.ResCatId))
					else:
						resource['ResCatId']=category.ResCatId
						print("resCat found, it's id: "+str(category.ResCatId))
				# /special synchronizer method

				try:
					if not 'ResId' in resource:
						print("No resId")
						newResource = Resource(**resource)
						db.session.add(newResource)
						db.session.commit()
						resources.append(resource)
					else:
						ResId = resource['ResId']
						thisResource = Resource.query.get(int(ResId))
						if thisResource is not None:
							print("update")
							# check for presenting in database
							thisResource.update(**resource)
							# thisResource.modifiedInfo(UId=1)
							db.session.commit()
							resources.append(resource)

						else:
							print("hasIDbutInsert")
							# create new resource
							newResource = Resource(**resource)
							db.session.add(newResource)
							db.session.commit()
							resources.append(resource)
				except:
					failed_resources.append(resource)

			status = checkApiResponseStatus(resources,failed_resources)
			res = {
				"data":resources,
				"fails":failed_resources,
				"success_total":len(resources),
				"fail_total":len(failed_resources)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)

	# elif request.method == 'PUT':
	# 	if not request.json:
	# 		res = {
	# 			"status": 0,
	# 			"message": "Error. Not a JSON data."
	# 		}
	# 		response = make_response(jsonify(res),400)
			
	# 	else:
	# 		req = request.get_json()
	# 		resources = []
	# 		failed_resources = [] 
	# 		for resource in req:
	# 			resource = addResourceDict(resource)
	# 			try:
	# 				ResId = resource['ResId']
	# 				thisResource = Resource.query.get(ResId)
	# 				thisResource.update(**resource)
	# 				thisResource.modifiedInfo(UId=1)
	# 				db.session.commit()
	# 				resources.append(resource)
	# 			except:
	# 				failed_resources.append(resource)

	# 		status = checkApiResponseStatus(resources,failed_resources)
	# 		res = {
	# 			"data":resources,
	# 			"fails":failed_resources,
	# 			"success_total":len(resources),
	# 			"fail_total":len(failed_resources)
	# 		}
	# 		for e in status:
	# 			res[e]=status[e]	
	# 		response = make_response(jsonify(res),200)

	# elif request.method == 'DELETE':
	# 	if not request.json:
	# 		res = {
	# 			"status": 0,
	# 			"message": "Error. Not a JSON data."
	# 		}
	# 		response = make_response(jsonify(res),400)
			
	# 	else:
	# 		req = request.get_json()
	# 		resources = []
	# 		failed_resources = [] 
	# 		for resource in req:
	# 			resource = addResourceDict(resource)
	# 			try:
	# 				ResId = resource['ResId']
	# 				thisResource = Resource.query.get(ResId)
	# 				thisResource.GCRecord = int(datetime.now().strftime("%H"))
	# 				thisResource.modifiedInfo(UId=1)
	# 				db.session.commit()
	# 				resources.append(resource)
	# 			except:
	# 				failed_resources.append(resource)

	# 		status = checkApiResponseStatus(resources,failed_resources)
	# 		res = {
	# 			"data":resources,
	# 			"fails":failed_resources,
	# 			"total":len(resources),
	# 			"success_total":len(resources),
	# 			"fail_total":len(failed_resources)
	# 		}
	# 		for e in status:
	# 			res[e]=status[e]
	# 		response = make_response(jsonify(res),200)
	
	return response