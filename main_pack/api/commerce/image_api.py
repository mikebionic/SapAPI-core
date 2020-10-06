# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus
from datetime import datetime

from main_pack.models.base.models import Image,Sl_image
from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addImageDict,saveImageFile
from main_pack import db
from main_pack.config import Config
from flask import send_from_directory
import dateutil.parser
import os
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-images/",methods=['GET','POST'])
@sha_required
def api_images():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		images = Image.query.filter_by(GCRecord = None)
		if DivId:
			images = images.filter_by(DivId = DivId)
		images = images.all()
		res = {
			"status": 1,
			"message": "All images",
			"data": [image.to_json_api() for image in images],
			"total": len(images)
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
			resources = Resource.query.filter_by(GCRecord = None).all()
			ResId_list = [resource.ResId for resource in resources]
			images = []
			failed_images = []
			for image in req:
				imageDictData = addImageDict(image)
				try:
					resource = ResId_list.index(imageDictData['ResId'])
					ImgRegNo = imageDictData['ImgRegNo']
					thisImage = Image.query\
						.filter_by(ImgRegNo = ImgRegNo)\
						.first()

					if thisImage is not None:
						updatingDate = dateutil.parser.parse(imageDictData['ModifiedDate'])
						if thisImage.ModifiedDate != updatingDate:
							print(f"{datetime.now()} | Image updated (Different ModifiedDate)")
							image = saveImageFile(image)
							thisImage.update(**image)
						# else:
						# 	print(f"{datetime.now()} | Image dropped (Same ModifiedDate)")
						images.append(imageDictData)
					else:
						image = saveImageFile(image)
						newImage = Image(**image)
						db.session.add(newImage)
						# print(f"{datetime.now()} | Image created")
						images.append(imageDictData)

				except Exception as ex:
					print(f"{datetime.now()} | Image Api Exception: {ex}")
					failed_images.append(imageDictData)

			db.session.commit()
			print(f"{datetime.now()} | Images were committed")
			status = checkApiResponseStatus(images,failed_images)
			res = {
				"data": images,
				"fails": failed_images,
				"success_total": len(images),
				"fail_total": len(failed_images)
			}
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),201)
	return response


@api.route("/get-image/<file_type>/<file_size>/<file_name>")
def get_image(file_type,file_size,file_name):
	if file_type == "slider": 
		sl_image = Sl_image.query.filter(Sl_image.SlImgMainImgFileName == file_name).first()
		path = sl_image.SlImgMainImgFilePath
	if file_type == "image": 
		image = Image.query.filter(Image.FileName == file_name).first()
		path = image.FilePath
	if file_size != 'undefined':
		path = path.replace("<FSize>",file_size)
	try:
		if Config.OS_TYPE == 'win32':
			response = send_from_directory('static',
				filename=path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=path.replace("<FSize>",file_size),as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)


@api.route("/get-file/<file_type>/<file_name>")
def get_file(file_type,file_name):
	if file_type == "slider": 
		sl_image = Sl_image.query.filter(Sl_image.SlImgMainImgFileName == file_name).first()
		path = sl_image.SlImgMainImgFilePath
	try:
		if Config.OS_TYPE == 'win32':
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
		if Config.OS_TYPE == 'win32':
			response = send_from_directory('static',filename=full_icon_path.replace("\\","/"),as_attachment=True)
		else:
			response = send_from_directory('static',filename=full_icon_path,as_attachment=True)
		return response
	except FileNotFoundError:
		abort(404)
