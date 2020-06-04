from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Res_category
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


@api.route("/v-resources/",methods=['GET'])
def api_resources_pack():
	if request.method == 'GET':
		resources = Resource.query.all()
		barcodes = Barcode.query.all()
		categories = Res_category.query.all()
		res_prices = Res_price.query.all()
		res_totals = Res_total.query.all()
		images = Image.query.all()
		data = []
		for resource in resources:
			resourceList = resource.to_json_api()
			resourceList["Barcode"] = [barcode.to_json_api() for barcode in barcodes if barcode.ResId==resource.ResId]
			resourceList["Res_category"] = [category.to_json_api() for category in categories if category.ResCatId==resource.ResCatId]
			resourceList["Res_price"] = [res_price.to_json_api() for res_price in res_prices if res_price.ResId==resource.ResId]
			resourceList["Res_total"] = [res_total.to_json_api() for res_total in res_totals if res_total.ResId==resource.ResId]
			resourceList["Image"] = [image.to_json_api() for image in images if image.ResId==resource.ResId]

			data.append(resourceList)
		res = {
			"status":1,
			"message":"All view resources",
			"data":data,
			"total":len(resources)
		}
		response = make_response(jsonify(res),200)
	return response

import base64

@api.route("/v-sm-resources/",methods=['GET'])
def api_resources_short():
	if request.method == 'GET':
		resources = Resource.query.all()
		barcodes = Barcode.query.all()
		categories = Res_category.query.all()
		res_prices = Res_price.query.all()
		res_totals = Res_total.query.all()
		images = Image.query.all()
		data = []
		for resource in resources:
			resourceList = resource.to_json_api()

			List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
			List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
			List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
			List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
			List_Image = [base64.encodebytes(image.Image).decode('ascii') for image in images if image.ResId==resource.ResId]

			resourceList["Barcode"] = List_Barcode[0] if len(List_Barcode)>0 else ''
			resourceList["Res_category"] = List_Res_category[0] if len(List_Res_category)>0 else ''
			resourceList["Res_price"] = List_Res_price[0] if len(List_Res_price)>0 else ''
			resourceList["Res_total"] = List_Res_total[0] if len(List_Res_total)>0 else ''
			resourceList["Image"] = List_Image[0] if len(List_Image)>0 else ''
			data.append(resourceList)
		res = {
			"status":1,
			"message":"All view resources",
			"data":data,
			"total":len(resources)
		}
		response = make_response(jsonify(res),200)
	return response
