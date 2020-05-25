from flask import render_template,jsonify,request,abort,make_response
from main_pack.api.commerce import api

from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addResourceDict

@api.route("/resources/<int:id>/",methods=['GET','PUT'])
def api_resource(id):
	if request.method == 'GET':
		resource = Resource.query.get(id)
		response = jsonify({'resource':resource.to_json_api()})
		res = {
			"status": "success",
			"data":{
				"resource":resource.to_json_api(),
			}
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		resource = Resource.query.get(id)
		updateResource = addResourceDict(req)
		resource.update(**resource)
		res = {
			"status": "success",
			"message": "resource updated",
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
			"status": "success",
			"message": "All resources",
			"data":{
				"resources":[resource.to_json_api() for resource in resources],
			}
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			resources = []
			for resource in req['resources']:
				resource = addResourceDict(resource)
				resources.append(resource)
				# newResource = Resource(**resource)
				# db.session.add(newResource)
				# db.session.commit()
			res = {
				"status": "success",
				"message": "Resources added",
				"data":{
					"resources":resources,
				}
			}
			response = make_response(jsonify(res),200)

	elif request.method == 'PUT':
		if not request.json:
			abort(400)
		else:
			req = request.get_json()
			resources = []
			for resource in req['resources']:
				try:
					resource = addResourceDict(resource)
					
					# ResId = resource['ResId']
					# thisResource = Resource.query.get(ResId)
					# thisResource.update(**resource)
					# thisResource.modifiedInfo(UId=1)
					# db.session.commit()
					resources.append(resource)

				except:
					res = {
						"status": "error",
						"message": "Update failed",
					}
					response = make_response(jsonify(res),400)
					return response
			res = {
				"status": "success",
				"message": "Resources updated",
				"data":{
					"resources":resources,
				}
			}
			response = make_response(jsonify(res),200)

	elif request.method == 'DELETE':
		if not request.json or not 'ResId' in request.json:
			abort(400)
		else:
			req = request.get_json()
			try:
				ResId = req.get('ResId')
				resource = Resource.query.get_or_404(ResId)
				resource.GCRecord = int(datetime.now().strftime("%H"))
				resource.modifiedInfo(UId=1)
				db.session.commit()
				res = {
					"status": "success",
					"message": "resource deleted",
				}
				response = make_response(jsonify(res),400)
			except:
				res = {
					"status": "error",
					"message": "Deletion failed, no change",
				}
				response = make_response(jsonify(res),400)
	
	return response