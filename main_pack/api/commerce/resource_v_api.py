from flask import jsonify,request,abort,make_response,url_for
from main_pack.api.commerce import api
from main_pack import db
from sqlalchemy import and_

from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.models.commerce.models import Resource

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
	resource_list = [{'ResId':ResId}]
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
		.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
			Resource.ResCatId==ResCatId).all()
	resource_list = []
	for resource in resources:
		product = {}
		product['ResId'] = resource.ResId
		resource_list.append(product)

	res = apiResourceInfo(resource_list)
	response = make_response(jsonify(res),200)
	return response

###### pagination #######
@api.route("/paginate/v-resources/",methods=['GET'])
def api_paginate_resources():
	latestResource = Resource.query\
		.filter(Resource.GCRecord=='' or Resource.GCRecord==None)\
		.order_by(Resource.ResId.desc())\
		.first()
	last = request.args.get('last',None,type=int)
	limit = request.args.get('limit',10,type=int)
	# handles the latest resource
	if last is None:
		last = latestResource.ResId+1

	pagination = Resource.query\
	.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None,Resource.ResId<last))\
	.order_by(Resource.ResId.desc())\
	.paginate(
		per_page=limit,
		error_out=False
		)
	# .order_by(Resource.ResId.desc())\
	resources = pagination.items
	prev = None

	### Gotta check it ######
	nextLast = Resource.query\
		.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None,Resource.ResId<(last-limit+1)))\
		.order_by(Resource.ResId.desc())\
		.first()
	prevLast = Resource.query\
		.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None,Resource.ResId<(last+limit+1)))\
		.order_by(Resource.ResId.desc())\
		.first()
	print(prevLast.ResId)
	if nextLast:
		prev = url_for('commerce_api.api_paginate_resources',last=prevLast.ResId,limit=limit)
	next = None
	if prevLast:
		next = url_for('commerce_api.api_paginate_resources',last=nextLast.ResId,limit=limit)
	
	resource_list = []
	for resource in pagination.items:
		product = {}
		product['ResId'] = resource.ResId
		resource_list.append(product)
	res = apiResourceInfo(resource_list)

	res = {
		"status":1,
		"message":"Paginated resources",
		"data":res['data'],
		"total":len(resources),
		'prev_url':prev,
		'next_url':next,
		'pages_total':pagination.total
	}
	return jsonify(res)