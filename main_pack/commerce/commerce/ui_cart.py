from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.commerce.commerce.utils import commonUsedData,realResRelatedData
from main_pack.models.commerce.models import Resource,Res_category


from main_pack.models.base.models import Company

# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####
from main_pack.models.base.models import Language
from main_pack.models.commerce.models import Color,Size,Brand

from main_pack.models.commerce.models import Resource 

from main_pack.base.apiMethods import fileToURL

def UiResourceData():
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

	data = []
	for resource in resources:
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if len(List_Barcode)>0 else ''
		resourceList["ResCatName"] = List_Res_category[0] if len(List_Res_category)>0 else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if len(List_Res_price)>0 else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if len(List_Res_total)>0 else ''
		resourceList["FilePathS"] = fileToURL('S',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathM"] = fileToURL('M',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathR"] = fileToURL('R',List_FileName[0]) if len(List_FileName)>0 else ''

		resourceList["Colors"] = List_Colors if len(List_Colors)>0 else ''
		resourceList["Sizes"] = List_Sizes if len(List_Sizes)>0 else ''
		resourceList["Brand"] = List_Brands[0] if len(List_Brands)>0 else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}

	return res


def UiSingleResourceData(resId):
	resource = Resource.query.get(resId)
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

	################
	resourceList = resource.to_json_api()

	List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
	List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
	List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
	List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
	List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

	List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
	List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
	List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

	resourceList["BarcodeVal"] = List_Barcode[0] if len(List_Barcode)>0 else ''
	resourceList["ResCatName"] = List_Res_category[0] if len(List_Res_category)>0 else ''
	resourceList["ResPriceValue"] = List_Res_price[0] if len(List_Res_price)>0 else ''
	resourceList["ResTotBalance"] = List_Res_total[0] if len(List_Res_total)>0 else ''
	resourceList["FilePathS"] = fileToURL('S',List_FileName[0]) if len(List_FileName)>0 else ''
	resourceList["FilePathM"] = fileToURL('M',List_FileName[0]) if len(List_FileName)>0 else ''
	resourceList["FilePathR"] = fileToURL('R',List_FileName[0]) if len(List_FileName)>0 else ''

	resourceList["Colors"] = List_Colors if len(List_Colors)>0 else ''
	resourceList["Sizes"] = List_Sizes if len(List_Sizes)>0 else ''
	resourceList["Brand"] = List_Brands[0] if len(List_Brands)>0 else ''

	data.append(resourceList)
	#############
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}
	
	return res

def UiMultiResourceData(product_list):
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
		print(product["resId"])
		resource = Resource.query.get(product["resId"])
		################
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if len(List_Barcode)>0 else ''
		resourceList["ResCatName"] = List_Res_category[0] if len(List_Res_category)>0 else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if len(List_Res_price)>0 else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if len(List_Res_total)>0 else ''
		resourceList["FilePathS"] = fileToURL('S',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathM"] = fileToURL('M',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathR"] = fileToURL('R',List_FileName[0]) if len(List_FileName)>0 else ''

		resourceList["Colors"] = List_Colors if len(List_Colors)>0 else ''
		resourceList["Sizes"] = List_Sizes if len(List_Sizes)>0 else ''
		resourceList["Brand"] = List_Brands[0] if len(List_Brands)>0 else ''

		resourceList["productQty"] = product["productQty"]
		data.append(resourceList)
	#############
	res = {
		"status":1,
		"data":data,
		"total":len(data)
	}
	
	return res


@bp.route("/product/ui_cart/", methods=['POST','PUT'])
def ui_cart():
	commonData = commonUsedData()
	if request.method == "POST":
		product_list=[]
		try:
			req = request.get_json()
			resId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['resId'] = resId
			product['productQty'] = productQty
			product_list.append(product)


			# resource = Resource.query.get(resId)
			resData = UiMultiResourceData(product_list)

			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					**commonData,**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
		product_list=[]
		req = request.get_json()

		# try:

		for resElement in req:
			resId = req[resElement].get('resId')
			productQty = req[resElement].get('productQty')
			
			product={}
			product['resId'] = resId
			product['productQty'] = productQty
			product_list.append(product)

		resData = UiMultiResourceData(product_list)

		response = jsonify({
			'status':'added',
			'responseText':gettext('Product')+' '+gettext('successfully saved!'),
			'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
				**commonData,**resData)
			})
		# except:
		# 	response = jsonify({
		# 		'status':'error',
		# 		'responseText':gettext('Unknown error!'),
		# 		})
	return response

















# @bp.route("/product/ui_cart/", methods=['POST','PUT'])
# def ui_cart():
# 	commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	if request.method == "POST":
# 		try:
# 			req = request.get_json()
# 			resId = req.get('resId')
# 			productQty = req.get('productQty')
# 			resource = Resource.query.get(resId)
# 			resourceQty='single'
# 			response = jsonify({
# 				'status':'added',
# 				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
# 				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
# 					resource=resource,**commonData,**resData,resourceQty=resourceQty,
# 					productQty=productQty)
# 				})
# 		except:
# 			response = jsonify({
# 				'status':'error',
# 				'responseText':gettext('Unknown error!'),
# 				})

# 	elif request.method == "PUT":
# 		resources=[]
# 		# productQuantities=[]
# 		req = request.get_json()
# 		try:
# 			for resElement in req:
# 				resId = req[resElement].get('resId')
# 				productQty = req[resElement].get('productQty')
				
# 				product={}
# 				product['resource'] = Resource.query.get(resId)
# 				# resources.append(resource)
# 				product['productQty'] = productQty
# 				resources.append(product)
# 			resourceQty='multi'
# 			response = jsonify({
# 				'status':'added',
# 				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
# 				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
# 					resources=resources,**commonData,**resData,resourceQty=resourceQty)
# 				})
# 		except:
# 			response = jsonify({
# 				'status':'error',
# 				'responseText':gettext('Unknown error!'),
# 				})
# 	return response


@bp.route("/product/ui_cart_table/", methods=['POST','PUT'])
def ui_cart_table():
	commonData = commonUsedData()
	resData = realResRelatedData()
	if request.method == "POST":
		try:
			req = request.get_json()
			resId = req.get('resId')
			productQty = req.get('productQty')
			resource = Resource.query.get(resId)
			resourceQty='single'
			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
					resource=resource,**commonData,**resData,resourceQty=resourceQty,
					productQty=productQty)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
		resources=[]
		req = request.get_json()
		# try:
		for resElement in req:
			print(resElement)
			resId = req[resElement].get('resId')
			productQty = req[resElement].get('productQty')
			product={}
			product['resource'] = Resource.query.get(resId)
			product['productQty'] = productQty
			resources.append(product)
			print(resources)
		resourceQty='multi'
		response = jsonify({
			'status':'added',
			'responseText':gettext('Product')+' '+gettext('successfully saved!'),
			'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
				resources=resources,**commonData,**resData,resourceQty=resourceQty)
			})
		# except:
		# 	response = jsonify({
		# 		'status':'error',
		# 		'responseText':gettext('Unknown error!'),
		# 		})
	return response