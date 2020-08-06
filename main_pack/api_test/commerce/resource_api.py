from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api_test.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models_test.commerce.models import Res_category
from main_pack.models_test.commerce.models import Resource
from main_pack.api_test.commerce.utils import addResourceDict
from main_pack import db_test
from flask import current_app
from main_pack.api_test.auth.api_login import sha_required

from main_pack.api_test.commerce.commerce_utils import apiResourceInfo

@api.route("/tbl-dk-resources/<int:ResId>/")
@sha_required
def api_resource(ResId):
	resource_list = [{'ResId':ResId}]
	res = apiResourceInfo(resource_list,single_object=True,isInactive=True,fullInfo=True)
	if res['status']==1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)

	# elif request.method == 'PUT':
	# 	resource = Resource.query.get(ResId)
	# 	# miguelGrinberg's method
	# 	# resource.from_json(request.json)
	# 	updateResource = addResourceDict(req)
	# 	resource.update(**resource)
	# 	res = {
	# 		"status": 1,
	# 		"message": "Resource updated",
	# 		"data": resource.to_json_api()
	# 	}
	# 	response = make_response(jsonify(res),200)
	return response

@api.route("/tbl-dk-resources/",methods=['GET','POST'])
@sha_required
def api_resources():
	if request.method == 'GET':
		res = apiResourceInfo(isInactive=True,fullInfo=True)
		if res['status']==0:
			status_code = 404
		else:
			status_code = 200
		response = make_response(jsonify(res),status_code)

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
				# category is resource's AddInf2
				group = resource['AddInf2']
				if group:
					category = Res_category.query.filter_by(ResCatName=group).first()
					if not category:
						category = Res_category(ResCatName=group)
						db_test.session.add(category)
						db_test.session.commit()
						resource['ResCatId']=category.ResCatId
					else:
						resource['ResCatId']=category.ResCatId
				# /special synchronizer method

				# check that UsageStatusId specified
				if resource['UsageStatusId']==None or '':
					resource['UsageStatusId']=2

				try:
					if not 'ResId' in resource:
						newResource = Resource(**resource)
						db_test.session.add(newResource)
						db_test.session.commit()
						resources.append(resource)
					else:
						ResId = resource['ResId']
						thisResource = Resource.query.get(int(ResId))
						# check for presenting in database
						if thisResource is not None:
							thisResource.update(**resource)
							# thisResource.modifiedInfo(UId=1)
							db_test.session.commit()
							resources.append(resource)

						else:
							# create new resource
							newResource = Resource(**resource)
							db_test.session.add(newResource)
							db_test.session.commit()
							resources.append(resource)
				except Exception as ex:
					failed_resources.append(resource)

			status = checkApiResponseStatus(resources,failed_resources)
			res = {
				"data": resources,
				"fails": failed_resources,
				"success_total": len(resources),
				"fail_total": len(failed_resources)
			}
			for e in status:
				res[e]=status[e]
			if res['status']==0:
				status_code = 400
			else:
				status_code = 201
				
			response = make_response(jsonify(res),status_code)

	return response