# -*- coding: utf-8 -*-
from flask import jsonify, request, abort, make_response
from flask import send_from_directory
from flask import current_app
import os
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload

from main_pack import db
from main_pack.config import Config
from . import api
from .utils import addImageDict, saveImageFile
from main_pack.api.auth.utils import sha_required, token_required
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.base.validators import request_is_json

from main_pack.models import Image, Sl_image
from main_pack.models import Resource, Barcode


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
	EmpId = None,
	BrandId = None,
	CId = None,
	RpAccId = None,
	ResId = None,
	ResCatId = None,
	ProdId = None,
	users = None,
	brands = None,
	resources = None,
	rp_accs = None,
	prods = None,
	employees = None,
	categories = None,
	companies = None
):

	filtering = {"GCRecord": None}

	if UId:
		filtering["UId"] = UId
	if EmpId:
		filtering["EmpId"] = EmpId
	if BrandId:
		filtering["BrandId"] = BrandId
	if CId:
		filtering["CId"] = CId
	if RpAccId:
		filtering["RpAccId"] = RpAccId
	if ResId:
		filtering["ResId"] = ResId
	if ResCatId:
		filtering["ResCatId"] = ResCatId
	if ProdId:
		filtering["ProdId"] = ProdId

	images = Image.query.filter_by(**filtering)

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

	if (resources or brands or rp_accs or categories or users or employees or companies or prods):
		images = images.filter(
			or_(
				Image.ResId != None if resources else Image.ResId == 0,
				Image.RpAccId != None if rp_accs else Image.RpAccId == 0,
				Image.BrandId != None if brands else Image.BrandId == 0,
				Image.ResCatId != None if categories else Image.ResCatId == 0,
				Image.EmpId != None if employees else Image.EmpId == 0,
				Image.UId != None if users else Image.UId == 0,
				Image.CId != None if companies else Image.CId == 0,
				Image.ProdId != None if prods else Image.ProdId == 0,
			))

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
def api_v_images(user):
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"EmpId": request.args.get("empId",None,type=int),
		"BrandId": request.args.get("brandId",None,type=int),
		"CId": request.args.get("companyId",None,type=int),
		"UId": request.args.get("userId",None,type=int),
		"RpAccId": request.args.get("rpAccId",None,type=int),
		"ResId": request.args.get("resId",None,type=int),
		"ResCatId": request.args.get("categoryId",None,type=int),
		"ProdId": request.args.get("prodId",None,type=int),
		"users": request.args.get("users",None,type=int),
		"brands": request.args.get("brands",None,type=int),
		"resources": request.args.get("resources",None,type=int),
		"rp_accs": request.args.get("rp_accs",None,type=int),
		"prods": request.args.get("prods",None,type=int),
		"employees": request.args.get("employees",None,type=int),
		"categories": request.args.get("categories",None,type=int),
		"companies": request.args.get("companies",None,type=int)
	}

	data = get_images(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Images",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/tbl-dk-images/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_images():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"notDivId": request.args.get("notDivId",None,type=int),
			"synchDateTime": request.args.get("synchDateTime",None,type=str),
			"EmpId": request.args.get("empId",None,type=int),
			"BrandId": request.args.get("brandId",None,type=int),
			"CId": request.args.get("companyId",None,type=int),
			"UId": request.args.get("userId",None,type=int),
			"RpAccId": request.args.get("rpAccId",None,type=int),
			"ResId": request.args.get("resId",None,type=int),
			"ResCatId": request.args.get("categoryId",None,type=int),
			"ProdId": request.args.get("prodId",None,type=int),
			"users": request.args.get("users",0,type=int),
			"brands": request.args.get("brands",0,type=int),
			"resources": request.args.get("resources",0,type=int),
			"rp_accs": request.args.get("rp_accs",0,type=int),
			"prods": request.args.get("prods",0,type=int),
			"employees": request.args.get("employees",0,type=int),
			"categories": request.args.get("categories",0,type=int),
			"companies": request.args.get("companies",0,type=int)
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

		# db.session.commit()
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
	try:
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

	except:
		abort(404)


@api.route("/get-file/<file_type>/<file_name>")
def get_file(file_type,file_name):
	try:
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
	except:
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
