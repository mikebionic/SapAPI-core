from flask import jsonify,request,abort,make_response,url_for
from main_pack.api_test.commerce import api
from main_pack import db_test
from sqlalchemy import and_,or_

# functions
from main_pack.api_test.commerce.commerce_utils import apiResourceInfo
# / functions /

# db Models
from main_pack.models_test.commerce.models import (Resource,
																							Barcode)
# / db Models /

@api.route("/v-full-resources/")
def api_v_full_resources():
	res = apiResourceInfo(fullInfo=True)
	response = make_response(jsonify(res),200)
	return response

@api.route("/v-resources/")
def api_v_resources():
	res = apiResourceInfo()
	response = make_response(jsonify(res),200)
	return response

@api.route("/v-resources/<int:ResId>/")
def api_v_resource_info(ResId):
	resource_list = [{"ResId": ResId}]
	res = apiResourceInfo(resource_list,single_object=True)
	if res['status']==1:
		status_code = 200
	else:
		status_code = 404
	response = make_response(jsonify(res),status_code)
	return response

@api.route("/tbl-dk-categories/<int:ResCatId>/v-resources/")
def api_category_v_resources(ResCatId):
	resources = Resource.query\
		.filter(and_(
			Resource.GCRecord=='' or Resource.GCRecord==None),\
			Resource.UsageStatusId==1,\
			Resource.ResCatId==ResCatId).all()
	resource_list = []
	for resource in resources:
		product = {}
		product['ResId'] = resource.ResId
		resource_list.append(product)

	res = apiResourceInfo(resource_list)
	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response

# @api.route("/tbl-dk-categories/<int:ResCatId>/tbl-dk-resources/")
# def api_category_tbl_dk_resources(ResCatId):
# 	resources = Resource.query\
# 		.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
# 			Resource.UsageStatusId==1,\
# 			Resource.ResCatId==ResCatId).all()
# 	data = []
# 	for resource in resources:
# 		data.append(resource.to_json_api())

# 	res = {
# 		"status": 1,
# 		"data": data,
# 		"total": len(data)
# 	}
# 	response = make_response(jsonify(res),200)
# 	return response

@api.route("/v-resources/search/")
def api_v_resources_search():
	searching_tag = request.args.get('tag',"",type=str)
	searching_tag = "%{}%".format(searching_tag)

	barcodes = Barcode.query\
		.filter(and_(
			Barcode.GCRecord=='' or Barcode.GCRecord==None,\
			Barcode.BarcodeVal.ilike(searching_tag))).all()
	
	resources = Resource.query\
		.filter(and_(
			Resource.GCRecord=='' or Resource.GCRecord==None,\
			Resource.ResName.ilike(searching_tag),\
			Resource.UsageStatusId==1))\
		.order_by(Resource.ResId.desc()).all()

	resource_list = []
	if barcodes:
		for barcode in barcodes:
			resource_list.append(barcode.ResId)
	for resource in resources:
		resource_list.append(resource.ResId)

	# removes dublicates
	resource_list = list(set(resource_list))
	resource_list = [{"ResId": resourceId} for resourceId in resource_list]

	res = apiResourceInfo(resource_list)

	res = {
		"status": 1,
		"message": "Resource search results",
		"data": res['data'],
		"total": len(resource_list)
	}

	response = make_response(jsonify(res),200)
	return response

###### pagination #######
@api.route("/v-resources/paginate/",methods=['GET'])
def api_paginate_resources():
	offset = request.args.get('offset',None,type=int)
	limit = request.args.get('limit',10,type=int)
	# handles the latest resource
	if offset is None:
		latestResource = Resource.query\
			.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None,\
				Resource.UsageStatusId==1))\
			.order_by(Resource.ResId.desc())\
			.first()
		offset = latestResource.ResId+1

	pagination = Resource.query\
	.filter(and_(
		Resource.GCRecord=='' or Resource.GCRecord==None,\
		Resource.ResId<offset,\
		Resource.UsageStatusId==1))\
	.order_by(Resource.ResId.desc())\
	.paginate(
		per_page=limit,
		error_out=False
		)
	resources = pagination.items

	nextLast = Resource.query\
		.filter(and_(
			Resource.GCRecord=='' or Resource.GCRecord==None,\
			Resource.ResId<(offset-limit+1),\
			Resource.UsageStatusId==1))\
		.order_by(Resource.ResId.desc())\
		.first()
	prevLast = Resource.query\
		.filter(and_(
			Resource.GCRecord=='' or Resource.GCRecord==None,\
			Resource.ResId<(offset+limit+1),\
			Resource.UsageStatusId==1))\
		.order_by(Resource.ResId.desc())\
		.first()

	prev = None
	if prevLast:
		prev = url_for('commerce_api.api_paginate_resources',offset=prevLast.ResId,limit=limit)
	next = None
	if nextLast:
		next = url_for('commerce_api.api_paginate_resources',offset=nextLast.ResId,limit=limit)
	
	resource_list = []
	for resource in pagination.items:
		product = {}
		product['ResId'] = resource.ResId
		resource_list.append(product)
	res = apiResourceInfo(resource_list)

	res = {
		"status": 1,
		"message": "Paginated resources",
		"data": res['data'],
		"total": len(resources),
		"prev_url": prev,
		"next_url": next,
		"pages_total": pagination.total
	}
	return jsonify(res)
