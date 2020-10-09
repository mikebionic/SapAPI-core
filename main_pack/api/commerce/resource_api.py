# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.commerce.models import Res_category
from main_pack.models.commerce.models import Resource,Barcode
from main_pack.api.commerce.utils import addResourceDict,addBarcodeDict
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


@api.route("/synch-resources/",methods=['GET','POST'])
@sha_required
def api_synch_resources():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		resources = Resource.query.filter_by(GCRecord = None)
		if DivId:
			resources = resources.filter_by(DivId = DivId)		
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			resources = resources.filter(Resource.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		resources = resources.all()
		data = []
		for resource in resources:
			resource_info = resource.to_json_api()
			resource_info["Barcodes"] = [barcode.to_json_api() for barcode in resource.Barcode]
			data.append(resource_info)

		res = {
			"status": 1,
			"data": data,
			"message": "Resources for syncronizer",
			"total": len(data)
		}
		response = make_response(jsonify(res),200)

	elif request.metod == 'POST':
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
			for data in req:
				resource = addResourceDict(data)

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
						resources.append(resource)
					else:
						thisResource = Resource(**resource)
						db.session.add(thisResource)
						resources.append(resource)

					db.session.commit()

					barcodes = []
					failed_barcodes = []
					for barcode in data['Barcodes']:
						barcode = addBarcodeDict(barcode)
						try:
							UnitId = barcode['UnitId']
							thisBarcode = Barcode.query\
								.filter_by(ResId = thisResource.ResId, UnitId = UnitId)\
								.first()
							barcode['ResId'] = thisResource.ResId
							if thisBarcode:
								thisBarcode.update(**barcode)
								barcodes.append(barcode)
							else:
								newBarcode = Barcode(**barcode)
								db.session.add(newBarcode)
								barcodes.append(barcode)
						except Exception as ex:
							print(f"{datetime.now()} | Barcode Api Exception: {ex}")
							failed_barcodes.append(barcode)

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
