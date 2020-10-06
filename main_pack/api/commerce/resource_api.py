# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime

from main_pack.models.commerce.models import Res_category
from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addResourceDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required

from main_pack.api.commerce.commerce_utils import apiResourceInfo


@api.route("/tbl-dk-resources/<int:ResId>/")
@sha_required
def api_resource(ResId):
	resource_list = [{'ResId':ResId}]
	res = apiResourceInfo(resource_list,single_object=True,isInactive=True,fullInfo=True)
	if res['status'] == 1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)

	return response


@api.route("/tbl-dk-resources/",methods=['GET','POST'])
@sha_required
def api_resources():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		res = apiResourceInfo(isInactive=True,fullInfo=True,DivId=DivId)
		if res['status'] == 0:
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
					try:
						category = Res_category.query\
							.filter_by(GCRecord = None, ResCatName = group)\
							.first()
						if not category:
							new_category = Res_category(ResCatName = group)
							db.session.add(new_category)
							db.session.commit()
							newCategoryId = new_category.ResCatId
						else:
							newCategoryId = category.ResCatId
						resource['ResCatId'] = newCategoryId
					except Exception as ex:
						print(f"{datetime.now()} | Resource Api Exception: {ex}")
				# / special synchronizer method /

				# check that UsageStatusId specified
				if resource['UsageStatusId'] == None or resource['UsageStatusId'] == '':
					resource['UsageStatusId'] = 2

				try:
					ResRegNo = resource['ResRegNo']
					thisResource = Resource.query\
						.filter_by(ResRegNo = ResRegNo)\
						.first()
					if thisResource is not None:
						thisResource.update(**resource)
						# thisResource.modifiedInfo(UId=1)
						resources.append(resource)
					else:
						# create new resource
						newResource = Resource(**resource)
						db.session.add(newResource)
						resources.append(resource)
						# check for presenting in database
				except Exception as ex:
					print(f"{datetime.now()} | Resource Api Exception: {ex}")
					failed_resources.append(resource)
			db.session.commit()
			status = checkApiResponseStatus(resources,failed_resources)
			res = {
				"data": resources,
				"fails": failed_resources,
				"success_total": len(resources),
				"fail_total": len(failed_resources)
			}
			for e in status:
				res[e] = status[e]
			if res['status'] == 0:
				status_code = 200
			else:
				status_code = 201
				
			response = make_response(jsonify(res),status_code)

	return response
