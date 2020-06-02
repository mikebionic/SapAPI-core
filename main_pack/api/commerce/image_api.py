from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.base.models import Image
from main_pack.api.commerce.utils import addImageDict
from main_pack import db
from flask import current_app


@api.route("/images/",methods=['GET','POST','PUT'])
def api_images():
	if request.method == 'GET':
		images = Image.query.all()
		res = {
			"status":1,
			"message":"All images",
			"data":[image.to_json_api() for image in images],
			"total":len(images)
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
			print(req)
			images = []
			failed_images = [] 
			for image in req:
				image = addImageDict(image)
				try:
					if not 'ImgId' in image:
						newImage = Image(**image)
						db.session.add(newImage)
						db.session.commit()
						images.append(image)
					else:
						ImgId = image['ImgId']
						thisImage = Image.query.get(int(ImgId))
						if thisImage is not None:
							thisImage.update(**image)
							db.session.commit()
							images.append(image)

						else:
							newImage = Image(**image)
							db.session.add(newImage)
							db.session.commit()
							images.append(image)
				except:
					failed_images.append(image)

			status = checkApiResponseStatus(images,failed_images)
			res = {
				"data":images,
				"fails":failed_images,
				"success_total":len(images),
				"fail_total":len(failed_images)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)

	return response