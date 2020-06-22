from flask import jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus,fileToURL
from main_pack.base.dataMethods import apiCheckImageByte

from main_pack.models.commerce.models import Resource
from main_pack.api.commerce.utils import addResourceDict

from main_pack.models.commerce.models import Barcode
from main_pack.api.commerce.utils import addBarcodeDict

from main_pack.models.commerce.models import Res_category
from main_pack.api.commerce.utils import addCategoryDict

from main_pack.models.base.models import Image
from main_pack.api.commerce.utils import addImageDict

from main_pack.models.commerce.models import Res_price
from main_pack.api.commerce.utils import addResPriceDict

from main_pack.models.commerce.models import Res_total
from main_pack.api.commerce.utils import addResTotalDict

from main_pack import db
from flask import current_app

from main_pack.models.commerce.models import (Color,Size,Brand,Unit,Usage_status)
from main_pack.models.commerce.models import (Res_color,Res_size,Res_unit)
from main_pack.api.auth.api_login import token_required
from sqlalchemy import and_

@api.route("/v-full-resources/",methods=['GET'])
def api_v_full_resources():
	if request.method == 'GET':
		resources = Resource.query\
			.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
		barcodes = Barcode.query\
			.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
		categories = Res_category.query\
			.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
		res_prices = Res_price.query\
			.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
		res_totals = Res_total.query\
			.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
		images = Image.query\
			.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

		colors = Color.query\
			.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
		sizes = Size.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		brands = Brand.query\
			.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()
		res_colors = Res_color.query\
			.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
		res_sizes = Res_size.query\
			.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()
		usage_statuses = Usage_status.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		units = Unit.query\
			.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()
		data = []
		for resource in resources:
			resourceList = resource.to_json_api()
			resourceList["Barcode"] = [barcode.to_json_api() for barcode in barcodes if barcode.ResId==resource.ResId]
			resourceList["Res_category"] = [category.to_json_api() for category in categories if category.ResCatId==resource.ResCatId]
			resourceList["Res_price"] = [res_price.to_json_api() for res_price in res_prices if res_price.ResId==resource.ResId]
			resourceList["Res_total"] = [res_total.to_json_api() for res_total in res_totals if res_total.ResId==resource.ResId]
			resourceList["Image"] = [image.to_json_api() for image in images if image.ResId==resource.ResId]
			resourceList["Colors"] = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
			resourceList["Sizes"] = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
			resourceList["Brand"] = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
			resourceList["UsageStatus"] = [usage_status.to_json_api() for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
			resourceList["Unit"] = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]

			data.append(resourceList)
		res = {
			"status":1,
			"message":"All view resources",
			"data":data,
			"total":len(resources)
		}
		response = make_response(jsonify(res),200)
	return response

@api.route("/v-resources/",methods=['GET'])
@token_required
def api_v_resources(current_user):
	if request.method == 'GET':
		resources = Resource.query\
			.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
		barcodes = Barcode.query\
			.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
		categories = Res_category.query\
			.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
		res_prices = Res_price.query\
			.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
		res_totals = Res_total.query\
			.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
		images = Image.query\
			.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

		colors = Color.query\
			.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
		sizes = Size.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		brands = Brand.query\
			.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

		res_colors = Res_color.query\
			.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
		res_sizes = Res_size.query\
			.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

		usage_statuses = Usage_status.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		units = Unit.query\
			.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()

		data = []
		for resource in resources:
			resourceList = resource.to_json_api()

			List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
			List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
			List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
			List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
			# # we don't need this blob anymore
			# List_Image = [apiCheckImageByte(image.Image) for image in images if image.ResId==resource.ResId]
			List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]
			List_Colors = [color.ColorName for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
			List_Sizes = [size.SizeName for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
			List_Brands = [brand.BrandName for brand in brands if brand.BrandId==resource.BrandId]
			List_Usage_statuses = [usage_status.UsageStatusName_tkTM for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
			List_Units = [unit.UnitName_tkTM for unit in units if unit.UnitId==resource.UnitId]

			resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
			resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
			resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
			resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
			# resourceList["Image"] = List_Image[0] if len(List_Image)>0 else ''
			resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
			resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
			resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''
			resourceList["Colors"] = List_Colors if List_Colors else ''
			resourceList["Sizes"] = List_Sizes if List_Sizes else ''
			resourceList["Brand"] = List_Brands[0] if List_Brands else ''
			resourceList["Unit"] = List_Units[0] if List_Units else ''
			resourceList["UsageStatus"] = List_Usage_statuses[0] if List_Usage_statuses else ''

			data.append(resourceList)
		res = {
			"status":1,
			"message":"All view resources",
			"data":data,
			"total":len(data)
		}
		response = make_response(jsonify(res),200)
	return response


@api.route("/tbl-dk-categories/<int:ResCatId>/v-resources/",methods=['GET'])
def api_category_v_resources(ResCatId):
	if request.method == 'GET':
		resources = Resource.query.filter_by(ResCatId=ResCatId)\
			.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
		barcodes = Barcode.query.all()
		categories = Res_category.query.all()
		res_prices = Res_price.query.all()
		res_totals = Res_total.query.all()
		images = Image.query.all()
		
		colors = Color.query\
			.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
		sizes = Size.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		brands = Brand.query\
			.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()
		res_colors = Res_color.query\
			.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
		res_sizes = Res_size.query\
			.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()
		usage_statuses = Usage_status.query\
			.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
		units = Unit.query\
			.filter(Unit.GCRecord=='' or Unit.GCRecord==None).all()
		data = []
		for resource in resources:
			resourceList = resource.to_json_api()

			List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
			List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
			List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
			List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
			List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]
			List_Colors = [color.ColorName for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
			List_Sizes = [size.SizeName for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
			List_Brands = [brand.BrandName for brand in brands if brand.BrandId==resource.BrandId]
			List_Usage_statuses = [usage_status.UsageStatusName_tkTM for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
			List_Units = [unit.UnitName_tkTM for unit in units if unit.UnitId==resource.UnitId]

			resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
			resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
			resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
			resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
			resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
			resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
			resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''
			resourceList["Colors"] = List_Colors if List_Colors else ''
			resourceList["Sizes"] = List_Sizes if List_Sizes else ''
			resourceList["Brand"] = List_Brands[0] if List_Brands else ''
			resourceList["Unit"] = List_Units[0] if List_Units else ''
			resourceList["UsageStatus"] = List_Usage_statuses[0] if List_Usage_statuses else ''
			data.append(resourceList)
		res = {
			"status":1,
			"message":"All view resources of category",
			"data":data,
			"total":len(data)
		}
		response = make_response(jsonify(res),200)
	return response


###### pagination #######


def ApiPaginatedResList(product_list):
	barcodes = Barcode.query\
		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
	res_prices = Res_price.query\
		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
	res_totals = Res_total.query\
		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

	res_colors = Res_color.query\
		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
	res_sizes = Res_size.query\
		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

	data = []

	for product in product_list:
		resource = Resource.query.get(product["resId"])
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if List_Barcode else ''
		resourceList["ResCatName"] = List_Res_category[0] if List_Res_category else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if List_Res_price else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if List_Res_total else ''
		resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if List_FileName else ''
		resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if List_FileName else ''

		resourceList["Colors"] = List_Colors if List_Colors else ''
		resourceList["Sizes"] = List_Sizes if List_Sizes else ''
		resourceList["Brand"] = List_Brands[0] if List_Brands else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}
	return res

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
		prev = url_for('commerce_api.api_paginate_resources',last=nextLast.ResId,limit=limit)
	next = None
	if prevLast:
		next = url_for('commerce_api.api_paginate_resources',last=prevLast.ResId,limit=limit)
	

	product_list = []
	for resource in pagination.items:
		product = {}
		product['resId'] = resource.ResId
		product_list.append(product)
	res = ApiPaginatedResList(product_list)


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
