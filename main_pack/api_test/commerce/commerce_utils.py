# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response

# functions and methods
from main_pack.base.invoiceMethods import resource_config_check
from main_pack.base.apiMethods import checkApiResponseStatus,fileToURL
# functions and methods

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# db models
from main_pack.models_test.commerce.models import (Resource,
                                              Res_category,
																							Wish)
from main_pack.models_test.commerce.models import (Color,
                                              Size,
                                              Brand,
                                              Unit,
                                              Usage_status)
from main_pack.models_test.base.models import Currency
# / db models /

# orders and db methods
from main_pack.models_test.commerce.models import (Order_inv,
																							Order_inv_line,
																							Inv_status)
from main_pack.api_test.commerce.utils import (addOrderInvDict,
																					addOrderInvLineDict)
from sqlalchemy import and_, extract
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models_test.users.models import Rp_acc
from main_pack.api_test.users.utils import apiRpAccData
# / Rp_acc db Model and methods /

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /


# isInactive shows active resources with UsageStatusId = 1
# fullInfo shows microframework full info with Foreign tables
# single_object returns one resource in "data" instead of list 
def apiResourceInfo(resource_list=None,
										single_object=False,
										isInactive=False,
										fullInfo=False,
										user=None):
	categories = Res_category.query.filter_by(GCRecord = None).all()
	usage_statuses = Usage_status.query.filter_by(GCRecord = None).all()
	units = Unit.query.filter_by(GCRecord = None).all()
	brands = Brand.query.filter_by(GCRecord = None).all()
	colors = Color.query.filter_by(GCRecord = None).all()
	sizes = Size.query.filter_by(GCRecord = None).all()
	currencies = Currency.query.filter_by(GCRecord = None).all()
	# return wishlist info for authenticated user
	if current_user.is_authenticated:
		user=current_user
	if user:
		RpAccId = user.RpAccId
		wishes = Wish.query\
			.filter_by(GCRecord = None,RpAccId = RpAccId)\
			.all()
	
	resource_models = []
	# if list with "ResId" is not provided, return all resources
	if resource_list is None:
		resource_filtering = {
			"GCRecord": None,
		}
		if isInactive==False:
			resource_filtering["UsageStatusId"] = 1

		resources = Resource.query\
			.filter_by(**resource_filtering).all()
		for resource in resources:
			if resource_config_check(resource):
				resource_models.append(resource)
	else:
		for resource_index in resource_list:
			ResId = int(resource_index["ResId"])
			resource_filtering = {
				"ResId": ResId,
				"GCRecord": None,
			}
			if isInactive==False:
				resource_filtering["UsageStatusId"] = 1

			resource = Resource.query\
				.filter_by(**resource_filtering).first()
			if resource:
				if resource_config_check(resource):
					resource_models.append(resource)
		
	data = []
	fails = []
	for resource in resource_models:
		try:
			resource_info = resource.to_json_api()

			List_Res_category = [category.to_json_api() for category in categories if category.ResCatId == resource.ResCatId]
			List_Brands = [brand.to_json_api() for brand in brands if brand.BrandId == resource.BrandId]
			List_UsageStatus = [usage_status.to_json_api() for usage_status in usage_statuses if usage_status.UsageStatusId == resource.UsageStatusId]
			List_Units = [unit.to_json_api() for unit in units if unit.UnitId == resource.UnitId]
			List_Colors = [color.to_json_api() for res_color in resource.Res_color if res_color.GCRecord == None for color in colors if color.ColorId == res_color.ColorId]
			List_Sizes = [size.to_json_api() for res_size in resource.Res_size if res_size.GCRecord == None for size in sizes if size.SizeId == res_size.SizeId]
			
			List_Barcode = [barcode.to_json_api() for barcode in resource.Barcode if barcode.GCRecord == None]
			List_Res_price = [res_price.to_json_api() for res_price in resource.Res_price if res_price.ResPriceTypeId == 2 and res_price.GCRecord == None]
			try:
				List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == List_Res_price[0]['CurrencyId']]
			except:
				List_Currencies = []
			List_Res_total = [res_total.to_json_api() for res_total in resource.Res_total if res_total.GCRecord == None and res_total.WhId == 1]
			List_Images = [image.to_json_api() for image in resource.Image if image.GCRecord == None]
			List_Ratings = [rating.to_json_api() for rating in resource.Rating if rating.GCRecord == None]
			if user:
				List_Wish = [wish.to_json_api() for wish in wishes if wish.ResId == resource.ResId]
			else:
				List_Wish = []

			resource_info["BarcodeVal"] = List_Barcode[0]['BarcodeVal'] if List_Barcode else ''
			resource_info["ResCatName"] = List_Res_category[0]['ResCatName'] if List_Res_category else ''
			resource_info["ResPriceValue"] = List_Res_price[0]['ResPriceValue'] if List_Res_price else ''
			resource_info["CurrencyCode"] = List_Currencies[0]['CurrencyCode'] if List_Currencies else 'TMT'
			resource_info["ResTotBalance"] = List_Res_total[0]['ResTotBalance'] if List_Res_total else ''
			resource_info["ResPendingTotalAmount"] = List_Res_total[0]['ResPendingTotalAmount'] if List_Res_total else ''
			resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName'],url='commerce_api_test.get_image') if List_Images else ''
			resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName'],url='commerce_api_test.get_image') if List_Images else ''
			resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName'],url='commerce_api_test.get_image') if List_Images else ''
			resource_info["Images"] = List_Images if List_Images else []
			resource_info["Colors"] = List_Colors if List_Colors else []
			resource_info["Sizes"] = List_Sizes if List_Sizes else []
			resource_info["Brand"] = List_Brands[0] if List_Brands else []
			resource_info["Unit"] = dataLangSelector(List_Units[0]) if List_Units else []
			
			rating_values = [rating['RtRatingValue'] for rating in List_Ratings if List_Ratings]
			try:
				average_rating = sum(rating_values) / len(rating_values)
				average_rating = round(average_ratign,2)
			except Exception as ex:
				average_rating = 0

			resource_info["RtRatingValue"] = average_rating
			resource_info["Wished"] = True if List_Wish else False
			if fullInfo == True:
				resource_info["UsageStatus"] = dataLangSelector(List_UsageStatus[0]) if List_UsageStatus else []
				resource_info["Barcode"] = List_Barcode if List_Barcode else []
				resource_info["Res_category"] = List_Res_category[0] if List_Res_category else []
				resource_info["Res_price"] = List_Res_price[0] if List_Res_price else []
				resource_info["Currency"] = dataLangSelector(List_Currencies[0]) if List_Currencies else []
				resource_info["Res_total"] = List_Res_total[0] if List_Res_total else []
				resource_info["Rating"] = List_Ratings[0] if List_Ratings else []
			data.append(resource_info)
		except Exception as ex:
			print(ex)
			fails.append(resource.to_json_api())
			
	status = checkApiResponseStatus(data,fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		if len(fails) == 1:
			fails = fails[0]
	res = {
			"message": "Resources",
			"data": data,
			"fails": fails,
			"total": len(data),
			"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]
	return res

def UiCartResourceData(product_list):
	res = apiResourceInfo(product_list)
	data = []
	resources = res['data']
	for resource in resources:
		for product in product_list:
			if (int(resource['ResId'])==int(product['ResId'])):
				try:
					resource["productQty"] = product["productQty"]
				except Exception as ex:
					print(ex)
					resource["productQty"] = 1
		resource["productTotal"]=int(resource["productQty"])*int(resource["ResPriceValue"])
		data.append(resource)
	res = {
		"status": 1,
		"data": data,
		"total": len(data)
	}
	return res

def apiOrderInvInfo(startDate=None,
										endDate=datetime.now(),
										statusId=None,
										single_object=False,
										invoice_list=None,
										rp_acc_user=None):
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()

	order_filtering = {
		"GCRecord": None
	}
	if statusId:
		order_filtering['InvStatId'] = statusId
	if rp_acc_user:
		order_filtering['RpAccId'] = rp_acc_user.RpAccId

	order_inv_models = []
	if invoice_list is None:
		if startDate == None:
			order_invoices = Order_inv.query\
				.filter_by(**order_filtering)\
				.order_by(Order_inv.OInvDate.desc()).all()
		else:
			# filtering by date
			if (type(startDate)!=datetime):
				startDate = dateutil.parser.parse(startDate)
				startDate = datetime.date(startDate)
				print(startDate)
			if (type(endDate)!=datetime):
				print(type(endDate))
				endDate = dateutil.parser.parse(endDate)
				endDate = datetime.date(endDate)
				print(endDate)
			order_invoices = Order_inv.query\
			.filter_by(**order_filtering)\
			.filter(and_(
				extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
				extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
				extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))\
			.order_by(Order_inv.OInvDate.desc()).all()
		for order_inv in order_invoices:
			order_inv_models.append(order_inv)
	else:
		for invoice_index in invoice_list:
			OInvRegNo = invoice_index["OInvRegNo"]
			order_filtering["OInvRegNo"] = OInvRegNo
			order_inv = Order_inv.query\
				.filter_by(**order_filtering).first()
			if order_inv:
				order_inv_models.append(order_inv)

	data = []
	fails = []
	for order_inv in order_inv_models:
		try:
			order_inv_info = order_inv.to_json_api()

			inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_inv.InvStatId]
			inv_status = dataLangSelector(inv_status_list[0])
			order_inv_info['InvStatName'] = inv_status['InvStatName']

			if rp_acc_user:
				rpAccData = apiRpAccData(dbModel=rp_acc_user)
			else:
				rp_acc = Rp_acc.query.filter_by(
						GCRecord = None, RpAccId = order_inv.RpAccId).first()
				rpAccData = apiRpAccData(dbModel=rp_acc)
			order_inv_info['Rp_acc'] = rpAccData['data']

			order_inv_info['Order_inv_lines'] = [order_inv_line.to_json_api() for order_inv_line in order_inv.Order_inv_line if order_inv_line.GCRecord == None]
			data.append(order_inv_info)
		except Exception as ex:
			print(ex)
			fails.append(order_inv.to_json_api())
	status = checkApiResponseStatus(data,fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		if len(fails) == 1:
			fails = fails[0]
	res = {
			"message": "Order invoice",
			"data": data,
			"fails": fails,
			"total": len(data),
			"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]
	return res
