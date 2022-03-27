# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy.orm import joinedload

from main_pack import db, cache
from . import api

from main_pack.models import Company, Division
from main_pack.models import (
	Resource,
	Barcode,
	Res_category,
	Brand
)
from .utils import addResourceDict, addBarcodeDict
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json


@api.route("/tbl-dk-resources/",methods=['GET','POST'])
@admin_required
@request_is_json(request)
def api_tbl_dk_resources(user):
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		ResId = request.args.get("id",None,type=int)
		ResRegNo = request.args.get("regNo","",type=str)
		ResName = request.args.get("name","",type=str)

		filtering = {"GCRecord": None}

		if ResId:
			filtering["ResId"] = ResId
		if ResRegNo:
			filtering["ResRegNo"] = ResRegNo
		if ResName:
			filtering["ResName"] = ResName
		if DivId:
			filtering["DivId"] = DivId

		resources = Resource.query.filter_by(**filtering)\
			.options(
				joinedload(Resource.company),
				joinedload(Resource.division),
				joinedload(Resource.Barcode))

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
			resource_info["CGuid"] = resource.company.CGuid if resource.company and not resource.company.GCRecord else None
			resource_info["DivGuid"] = resource.division.DivGuid if resource.division and not resource.division.GCRecord else None
			resource_info["Barcodes"] = [barcode.to_json_api() for barcode in resource.Barcode if not barcode.GCRecord]
			data.append(resource_info)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"data": data,
			"message": "Resources",
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
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

		data = []
		failed_data = []

		for resource_req in req:
			resource_info = addResourceDict(resource_req)

			# special syncronizer method 
			# BrandName is resource's AddInf1
			BrandName = resource_info["AddInf1"]
			if BrandName:
				try:
					thisBrand = Brand.query\
						.filter_by(GCRecord = None, BrandName = BrandName)\
						.first()

					if not thisBrand:
						thisBrand = Brand(BrandName = BrandName)
						db.session.add(thisBrand)
						db.session.commit()

					resource_info["BrandId"] = thisBrand.BrandId

				except Exception as ex:
					print(f"{datetime.now()} | Resource Api Brand creation Exception: {ex}")

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
				
				data.append(resource_req)
				db.session.commit()

				barcodes = []
				failed_barcodes = []
				for barcode_req in resource_req["Barcodes"]:
					try:
						barcode_info = addBarcodeDict(barcode_req)
						UnitId = barcode_info["UnitId"]
						ResId = thisResource.ResId

						barcode_info["ResId"] = ResId
						barcode_info["CId"] = CId
						barcode_info["DivId"] = DivId

						thisBarcode = Barcode.query\
							.filter_by(
								ResId = ResId,
								UnitId = UnitId,
								BarcodeVal = barcode_info["BarcodeVal"],
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

				db.session.commit()

			except Exception as ex:
				print(f"{datetime.now()} | Resource Api Exception: {ex}")
				failed_data.append(resource_req)

		cache.clear()
		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response