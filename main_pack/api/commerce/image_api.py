# -*- coding: utf-8 -*-
from flask import jsonify, request, abort, make_response
from flask import send_from_directory
from flask import current_app
import os
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack import db
from main_pack.config import Config
from . import api
from .utils import addImageDict, saveImageFile
from main_pack.api.auth.utils import sha_required, token_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json

from main_pack.models.base.models import Image, Sl_image
from main_pack.models.commerce.models import Resource, Barcode


def remove_image(file_type,file_name):
	if file_type == "icon":
		file_type = "image"
		file_size = "undefined"
		file = get_image(file_type=file_type,file_size=file_size,file_name=file_name,path_only=True)
		FilePath = os.path.join(current_app.root_path,"static",file)
		os.remove(FilePath)
	else:
		file = get_image(file_type=file_type,file_size='S',file_name=file_name,path_only=True)
		FilePathS = os.path.join(current_app.root_path,"static",file)
		file = get_image(file_type=file_type,file_size='M',file_name=file_name,path_only=True)
		FilePathM = os.path.join(current_app.root_path,"static",file)
		file = get_image(file_type=file_type,file_size='R',file_name=file_name,path_only=True)
		FilePathR = os.path.join(current_app.root_path,"static",file)
		os.remove(FilePathS)
		os.remove(FilePathM)
		os.remove(FilePathR)


def get_images(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	UId = None,
	URegNo = None,
	UName = None):

	images = Image.query.filter_by(GCRecord = None)

	if DivId:
		images = images\
			.join(Resource, and_(
				Resource.ResId == Image.ResId,
				Resource.DivId == DivId))
	if notDivId:
		images = images\
			.join(Resource, and_(
				Resource.ResId == Image.ResId,
				Resource.DivId != notDivId))

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		images = images.filter(Image.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	images = images.options(
		joinedload(Image.resource),
		joinedload(Image.rp_acc))\
	.all()

	data = []
	for image in images:
		image_info = image.to_json_api()
		image_info["ResRegNo"] = image.resource.ResRegNo if image.resource and not image.resource.GCRecord else None
		image_info["ResGuid"] = image.resource.ResGuid if image.resource and not image.resource.GCRecord else None
		image_info["RpAccGuid"] = image.rp_acc.RpAccGuid if image.rp_acc and not image.rp_acc.GCRecord else None
		data.append(image_info)

	return data


@api.route("/v-images/")
@token_required
def api_v_images():
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str)
	}

	data = get_images(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Images",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)


@api.route("/tbl-dk-images/",methods=['GET','POST'])
@sha_required
@request_is_json
def api_images():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"notDivId": request.args.get("notDivId",None,type=int),
			"synchDateTime": request.args.get("synchDateTime",None,type=str)
		}

		data = get_images(**arg_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "All images",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		resources = Resource.query.filter_by(GCRecord = None).all()
		resource_ResId_list = [resource.ResId for resource in resources]
		resource_ResGuid_list = [str(resource.ResGuid) for resource in resources]
		# resource_RegNo_list = [resource.ResRegNo for resource in resources]

		data = []
		failed_data = []

		for image_req in req:
			try:
				ResRegNo = image_req["ResRegNo"]
				ResGuid = image_req["ResGuid"]

				if Config.USE_PROVIDED_IMAGE_FILENAME == True:
					thisResource = Resource.query\
						.filter_by(
							ResGuid = ResGuid,
							ResRegNo = ResRegNo,
							GCRecord = None)\
						.options(joinedload(Resource.Barcode))\
						.first()
					ResId = thisResource.ResId
					barcode = thisResource.Barcode[0]
					
					if (Config.PROVIDED_IMAGE_FILENAME_TYPE == 1):
						image_req["FileName"] = thisResource.ResName
						if (len(list(filter(lambda n: n in image_req["FileName"], Config.FILENAME_INVALID_CHARACTERS))) > 0):
							# barcode = Barcode.query.filter_by(ResId = ResId, GCRecord = None).first()
							image_req["FileName"] = barcode.BarcodeVal
					elif (Config.PROVIDED_IMAGE_FILENAME_TYPE == 2):
						image_req["FileName"] = barcode.BarcodeVal

				else:
					indexed_res_id = resource_ResId_list[resource_ResGuid_list.index(ResGuid)]
					ResId = int(indexed_res_id)
				image_req["ResId"] = ResId

				imageDictData = addImageDict(image_req)
				# print(f"trying image of {ResRegNo} of resourceId {ResId}")
				ImgGuid = imageDictData['ImgGuid']
				thisImage = Image.query\
					.filter_by(
						ImgGuid = ImgGuid,
						GCRecord = None)\
					.first()

				if thisImage is not None:
					updatingDate = dateutil.parser.parse(imageDictData['ModifiedDate'])
					if thisImage.ModifiedDate != updatingDate:
						image_data = saveImageFile(image_req)
						image_data['ImgId'] = thisImage.ImgId
						try:
							# Delete last image
							file_type = "image"
							file_name = thisImage.FileName
							remove_image(file_type,file_name)

						except Exception as ex:
							print(f"{datetime.now()} | Image Api Deletion Exception: {ex}")
						
						thisImage.update(**image_data)
						print(f"{datetime.now()} | Image updated (Different ModifiedDate)")

					else:
						print(f"{datetime.now()} | Image dropped (Same ModifiedDate)")

					image_req["Image"] = None
					data.append(image_req)

				else:
					image_data = saveImageFile(image_req)
					thisImage = Image(**image_data)
					db.session.add(thisImage)

					try:
						db.session.commit()
					except Exception as ex:
						print(f"{datetime.now()} | Couldn't commit: {ex}")

						try:
							lastImage = Image.query.order_by(Image.ImgId.desc()).first()
							ImgId = lastImage.ImgId+1
						except:
							ImgId = None

						thisImage.ImgId = ImgId
						db.session.add(thisImage)
						db.session.commit()

					print(f"{datetime.now()} | Image created")
					image_req["Image"] = None
					data.append(image_req)

			except Exception as ex:
				print(f"{datetime.now()} | Image Api Exception: {ex}")
				image_req["Image"] = None
				failed_data.append(image_req)

		db.session.commit()
		print(f"{datetime.now()} | Images were committed")
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


@api.route("/get-image/<file_type>/<file_size>/<file_name>")
def get_image(file_type,file_size,file_name,path_only=False):
	if file_type == "slider": 
		sl_image = Sl_image.query.filter(Sl_image.SlImgMainImgFileName == file_name).first()
		path = sl_image.SlImgMainImgFilePath
	if file_type == "image": 
		image = Image.query.filter(Image.FileName == file_name).first()
		if not image.FilePath:
			raise FileNotFoundError
		path = image.FilePath
	if file_size != 'undefined':
		path = path.replace("<FSize>",file_size)
	try:
		if Config.OS_TYPE == 'win32':
			full_path = path.replace("\\","/")
		else:
			full_path = path.replace("<FSize>",file_size)
		
		response = send_from_directory('static',full_path,as_attachment=True)
		if path_only:
			return full_path
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
