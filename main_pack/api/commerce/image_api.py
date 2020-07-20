from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.base.models import Image,Sl_image
from main_pack.api.commerce.utils import addImageDict,saveImageFile
from main_pack import db
from flask import current_app,send_from_directory
import dateutil.parser
import os
from main_pack.api.auth.api_login import sha_required

@api.route("/tbl-dk-images/",methods=['GET','POST','PUT'])
@sha_required
def api_images():
	if request.method == 'GET':
		images = Image.query\
			.filter(Image.GCRecord=='' or Image.GCRecord==None).all()
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
			images = []
			failed_images = []
			for image in req:
				imageDictData = addImageDict(image)
				try:
					if not 'ImgId' in imageDictData:
						image = saveImageFile(image)
						newImage = Image(**image)
						db.session.add(newImage)
						db.session.commit()
						print('added cuz no ImageId provided')
						images.append(image)
					else:
						ImgId = imageDictData['ImgId']
						thisImage = Image.query.get(int(ImgId))
						
						updatingDate = dateutil.parser.parse(imageDictData['ModifiedDate'])
						if thisImage is not None:
							print("image is not none")
							if thisImage.ModifiedDate!=updatingDate:
								print('updated cuz different ModifiedDate')
								image = saveImageFile(image)
								thisImage.update(**image)
								db.session.commit()
								images.append(image)
							else:
								print("same modified date")
						else:
							image = saveImageFile(image)
							newImage = Image(**image)
							db.session.add(newImage)
							db.session.commit()
							print('added image was none')
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
			response = make_response(jsonify(res),201)
	return response



@api.route("/get-image/<image_size>/<image_name>")
def get_image(image_size,image_name):
	image = Image.query.filter(Image.FileName==image_name).first()
	if image_size=='M':
		path = image.FilePathM
	elif image_size=='S':
		path = image.FilePathS
	elif image_size=="R":
		path = image.FilePathR
	try:
		if current_app.config['OS_TYPE']=='win32':
			response = send_from_directory('static',filename=path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=path,as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)


@api.route("/get-image/<file_type>/<file_size>/<file_name>")
def get_image_test(file_type,file_size,file_name):
	if file_type=="slider":
		sl_image = Sl_image.query.filter(Sl_image.SlImgName==file_name).first()
		path = sl_image.SlImgMainImgFileName
	if file_type=="image":
		image = Image.query.filter(Image.FileName==file_name).first()
		path = image.FilePath
	if file_size != 'undefined':
		path = path.replace("<FSize>",file_size)
	try:
		if current_app.config['OS_TYPE']=='win32':
			response = send_from_directory('static',
				filename=path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=path.replace("<FSize>",file_size),as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)


@api.route("/get-file/<file_type>/<file_name>")
def get_file(file_type,file_name):
	if file_type=="slider":
		sl_image = Sl_image.query.filter(Sl_image.SlImgName==file_name).first()
		path = sl_image.SlImgMainImgFileName
	try:
		if current_app.config['OS_TYPE']=='win32':
			response = send_from_directory('static',filename=path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=path,as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)


@api.route("/get-icon/<category>/<file_name>")
def get_icon(category,file_name):
	icons_path = os.path.join("commerce","icons","categories")
	full_icon_path = os.path.join(icons_path,category,file_name)
	try:
		if current_app.config['OS_TYPE']=='win32':
			response = send_from_directory('static',filename=full_icon_path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=full_icon_path,as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)