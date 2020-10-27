# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models.base.models import Company, Division
from main_pack.models.commerce.models import Resource, Barcode, Res_category
from main_pack.api.commerce.utils import addResourceDict, addBarcodeDict
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
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		resources = Resource.query.filter_by(GCRecord = None)
		if DivId:
			resources = resources.filter_by(DivId = DivId)
		if notDivId:
			resources = resources.filter(Resource.DivId != notDivId)		
		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			resources = resources.filter(Resource.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))
		
		resources = resources.all()
		
		data = []
		for resource in resources:
			resource_info = resource.to_json_api()
			resource_info["CGuid"] = resource.company.CGuid if resource.company else None
			resource_info["DivGuid"] = resource.division.DivGuid if resource.division else None
			resource_info["Barcodes"] = [barcode.to_json_api() for barcode in resource.Barcode]
			data.append(resource_info)

		res = {
			"status": 1,
			"data": data,
			"message": "Resources for syncronizer",
			"total": len(data)
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

			companies = Company.query\
				.filter_by(GCRecord = None)\
				.filter(Company.CGuid != None).all()
			divisions = Division.query\
				.filter_by(GCRecord = None)\
				.filter(Division.DivGuid != None).all()

			division_DivId_list = [division.DivId for division in divisions]
			division_DivGuid_list = [str(division.DivGuid) for division in divisions]

			company_CId_list = [company.CId for company in companies]
			company_CGuid_list = [str(company.CGuid) for company in companies]

			resources = []
			failed_resources = []
			for resource_req in req:
				resource_info = addResourceDict(resource_req)

				# special syncronizer method 
				# ResCatName is resource's AddInf2
				ResCatName = resource_info["AddInf2"]
				if ResCatName:
					try:
						thisCategory = Res_category.query\
							.filter_by(GCRecord = None, ResCatName = ResCatName)\
							.first()
						if not thisCategory:
							thisCategory = Res_category(ResCatName = ResCatName)
							db.session.add(thisCategory)
							db.session.commit()
						
						resource_info["ResCatId"] = thisCategory.ResCatId
					except Exception as ex:
						print(f"{datetime.now()} | Resource Api Res_cateogry creation Exception: {ex}")
				# / special synchronizer method /

				# check that UsageStatusId specified
				if resource_info["UsageStatusId"] == None or resource_info["UsageStatusId"] == '':
					resource_info["UsageStatusId"] = 2

				try:
					ResRegNo = resource_info["ResRegNo"]
					ResGuid = resource_info["ResGuid"]

					DivGuid = resource_req["DivGuid"]
					CGuid = resource_req["CGuid"]

					try:
						indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
						DivId = int(indexed_div_id)
					except:
						DivId = None
					try:
						indexed_c_id = company_CId_list[company_CGuid_list.index(CGuid)]
						CId = int(indexed_c_id)
					except:
						CId = None

					resource_info["DivId"] = DivId
					resource_info["CId"] = CId

					thisResource = Resource.query\
						.filter_by(
							ResRegNo = ResRegNo,
							ResGuid = ResGuid,
							GCRecord = None)\
						.first()
					if thisResource:
						resource_info["ResId"] = thisResource.ResId
						thisResource.update(**resource_info)
					else:
						try:
							lastResource = Resource.query.order_by(Resource.ResId.desc()).first()
							ResId = lastResource.ResId+1
						except:
							ResId = None
						resource_info["ResId"] = ResId
						thisResource = Resource(**resource_info)
						db.session.add(thisResource)
					
					resources.append(resource_req)
					db.session.commit()

					barcodes = []
					failed_barcodes = []
					for barcode_req in resource_req["Barcodes"]:
						try:
							barcode_info = addBarcodeDict(barcode_req)
							UnitId = barcode_info["UnitId"]
							ResId = thisResource.ResId
							barcode_info["ResId"] = ResId
							thisBarcode = Barcode.query\
								.filter_by(
									ResId = ResId,
									UnitId = UnitId,
									GCRecord = None)\
								.first()
							if thisBarcode:
								barcode_info["BarcodeId"] = thisBarcode.BarcodeId
								thisBarcode.update(**barcode_info)
							else:
								thisBarcode = Barcode(**barcode_info)
								db.session.add(thisBarcode)
							barcodes.append(barcode_req)
						except Exception as ex:
							print(f"{datetime.now()} | Barcode Api Exception: {ex}")
							failed_barcodes.append(barcode_req)

				except Exception as ex:
					print(f"{datetime.now()} | Resource Api Exception: {ex}")
					failed_resources.append(resource_req)
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