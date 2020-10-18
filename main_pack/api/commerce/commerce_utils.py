# -*- coding: utf-8 -*-
from flask import jsonify,request,abort,make_response
from main_pack.config import Config

# functions and methods
from main_pack.base.apiMethods import checkApiResponseStatus,fileToURL
# functions and methods

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# db models
from main_pack.models.commerce.models import (Resource,
																							Res_price,
																							Res_total,
                                              Res_category,
																							Wish,
																							Rating)
from main_pack.models.commerce.models import (Color,
                                              Size,
                                              Brand,
                                              Unit,
                                              Usage_status)
from main_pack.models.base.models import Currency
# / db models /

# orders and db methods
from main_pack.models.commerce.models import (Order_inv,
																							Order_inv_line,
																							Invoice,
																							Inv_line,
																							Inv_status)
from sqlalchemy import and_, extract
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models.users.models import Rp_acc,Users
from main_pack.api.users.utils import apiRpAccData,apiUsersData
# / Rp_acc db Model and methods /

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime,timedelta
# / datetime, date-parser /


# showInactive shows active resources with UsageStatusId = 1
# fullInfo shows microframework full info with Foreign tables
# single_object returns one resource in "data" instead of list
# showRated gives you latest rated resources
# showLatest gives you latest resources by datetime
def apiResourceInfo(resource_list = None,
										single_object = False,
										showInactive = False,
										fullInfo = False,
										user = None,
										resource_models = None,
										showRelated = False,
										showLatest = False,
										showRated = False,
										avoidQtyCheckup = False,
										showNullPrice = False,
										DivId = None,
										notDivId = None):
	categories = Res_category.query.filter_by(GCRecord = None).all()
	usage_statuses = Usage_status.query.filter_by(GCRecord = None).all()
	units = Unit.query.filter_by(GCRecord = None).all()
	brands = Brand.query.filter_by(GCRecord = None).all()
	colors = Color.query.filter_by(GCRecord = None).all()
	sizes = Size.query.filter_by(GCRecord = None).all()
	currencies = Currency.query.filter_by(GCRecord = None).all()
	# return wishlist info for authenticated user
	if current_user.is_authenticated:
		user = current_user
	if user:
		RpAccId = user.RpAccId
		wishes = Wish.query\
			.filter_by(GCRecord = None, RpAccId = RpAccId)\
			.all()
	
	if not resource_models:
		resource_models = []
		# if list with "ResId" is not provided, return all resources
		if resource_list is None:
			resource_filtering = {
				"GCRecord": None,
			}
			if showInactive == False:
				resource_filtering["UsageStatusId"] = 1

			resources = Resource.query\
				.filter_by(**resource_filtering)

			if showNullPrice == False:
				resources = resources\
					.join(Res_price, Res_price.ResId == Resource.ResId)\
					.filter(Res_price.ResPriceValue > 0)
			if avoidQtyCheckup == False:
				if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:
					resources = resources\
						.join(Res_total, Res_total.ResId == Resource.ResId)\
						.filter(and_(
							Res_total.WhId == 1, 
							Res_total.ResTotBalance > 0))

			if showLatest == True:
				resources = resources\
					.order_by(Resource.CreatedDate.desc())\
					.limit(Config.RESOURCE_MAIN_PAGE_SHOW_QTY)

			if showRated == True:
				resources = resources\
					.join(Res_category, Res_category.ResCatId == Resource.ResCatId)\
					.filter(Res_category.IsMain == True)\
					.outerjoin(Rating, Rating.ResId == Resource.ResId)\
					.filter(Rating.RtRatingValue >= Config.SMALLEST_RATING_VALUE_SHOW)\
					.order_by(Rating.RtRatingValue.asc())\
					.limit(Config.RESOURCE_MAIN_PAGE_SHOW_QTY + 1)
			
			if DivId:
				resources = resources.filter(Resource.DivId == DivId)
			if notDivId:
				resources = resources.filter(Resource.DivId != notDivId)
			resources = resources.all()

			for resource in resources:
				resource_models.append(resource)

		else:
			for resource_index in resource_list:
				ResId = int(resource_index["ResId"])
				resource_filtering = {
					"ResId": ResId,
					"GCRecord": None,
				}
				if showInactive == False:
					resource_filtering["UsageStatusId"] = 1

				resource = Resource.query\
					.filter_by(**resource_filtering)
				
				if showNullPrice == False:
					resources = resources\
						.join(Res_price, Res_price.ResId == Resource.ResId)\
						.filter(Res_price.ResPriceValue > 0)
				
				if avoidQtyCheckup == False:
					if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:
						resource = resource\
							.join(Res_total, Res_total.ResId == Resource.ResId)\
							.filter(and_(
								Res_total.WhId == 1, 
								Res_total.ResTotBalance > 0))
				
				resource = resource.first()
				
				if resource:
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
			# Sorting list by Modified date
			List_Images = (sorted(List_Images, key = lambda i: i['ModifiedDate']))
			
			if fullInfo == True:
				List_Ratings = []
				for rating in resource.Rating:
					Rating_info = rating.to_json_api()
					if rating.UId:
						rated_user = Users.query\
							.filter_by(GCRecord = None, UId = rating.UId)\
							.first()
						userData = apiUsersData(dbModel=rated_user)
						Rating_info['User'] = userData['data']
					if rating.RpAccId:
						rated_rp_acc = Rp_acc.query\
							.filter_by(GCRecord = None, RpAccId = rating.RpAccId)\
							.first()
						rpAccData = apiRpAccData(dbModel=rated_rp_acc)
						Rating_info['Rp_acc'] = rpAccData['data']
					List_Ratings.append(Rating_info)
			else:
				List_Ratings = [rating.to_json_api() for rating in resource.Rating if rating.GCRecord == None]
			if user:
				List_Wish = [wish.to_json_api() for wish in wishes if wish.ResId == resource.ResId]
			else:
				List_Wish = []

			resource_info["BarcodeVal"] = List_Barcode[0]['BarcodeVal'] if List_Barcode else ''
			resource_info["ResCatName"] = List_Res_category[0]['ResCatName'] if List_Res_category else ''
			resource_info["ResPriceValue"] = List_Res_price[0]['ResPriceValue'] if List_Res_price else 0
			resource_info["CurrencyCode"] = List_Currencies[0]['CurrencyCode'] if List_Currencies else 'TMT'
			resource_info["ResTotBalance"] = List_Res_total[0]['ResTotBalance'] if List_Res_total else 0
			resource_info["ResPendingTotalAmount"] = List_Res_total[0]['ResPendingTotalAmount'] if List_Res_total else 0
			resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]['FileName']) if List_Images else ''
			resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]['FileName']) if List_Images else ''
			resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]['FileName']) if List_Images else ''
			resource_info["Images"] = List_Images if List_Images else []
			resource_info["Colors"] = List_Colors if List_Colors else []
			resource_info["Sizes"] = List_Sizes if List_Sizes else []
			resource_info["Brand"] = List_Brands[0] if List_Brands else []
			resource_info["Unit"] = dataLangSelector(List_Units[0]) if List_Units else []
			
			rating_values = [rating['RtRatingValue'] for rating in List_Ratings if List_Ratings]
			try:
				average_rating = sum(rating_values) / len(rating_values)
				average_rating = round(average_rating,2)
			except Exception as ex:
				average_rating = 0.0

			resource_info["RtRatingValue"] = average_rating
			resource_info["Wishlist"] = True if List_Wish else False
			resource_info["New"] = True if resource.CreatedDate >= datetime.today() - timedelta(days=Config.COMMERCE_RESOURCE_NEWNESS_DAYS) else False
			if showRelated == True:
				related_resources = Resource.query\
					.filter_by(GCRecord = None, ResCatId = resource.ResCatId)\
					.filter(Resource.ResId != resource.ResId)\
					.join(Res_total, Res_total.ResId == Resource.ResId)\
					.filter(and_(
						Res_total.WhId == 1, 
						Res_total.ResTotBalance > 0))\
					.outerjoin(Rating, Rating.ResId == Resource.ResId)\
					.order_by(Rating.RtRatingValue.asc())\
					.limit(Config.TOP_RATED_RESOURCES_AMOUNT+1)\
					.all()

				Related_resources = []
				for resource in related_resources:
					related_resource_info = resource.to_json_api()
					Related_resource_Images = [image.to_json_api() for image in resource.Image if image.GCRecord == None]
					related_resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=Related_resource_Images[-1]['FileName']) if Related_resource_Images else ''
					related_resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=Related_resource_Images[-1]['FileName']) if Related_resource_Images else ''
					related_resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=Related_resource_Images[-1]['FileName']) if Related_resource_Images else ''
					

					Related_resource_category = [category.to_json_api() for category in categories if category.ResCatId == resource.ResCatId]
					Related_resource_price = [res_price.to_json_api() for res_price in resource.Res_price if res_price.ResPriceTypeId == 2 and res_price.GCRecord == None]
					try:
						Related_resource_currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == Related_resource_price[0]['CurrencyId']]
					except:
						Related_resource_currencies = []
					related_resource_info["ResCatName"] = Related_resource_category[0]['ResCatName'] if Related_resource_category else ''
					related_resource_info["ResPriceValue"] = Related_resource_price[0]['ResPriceValue'] if Related_resource_price else ''
					related_resource_info["CurrencyCode"] = Related_resource_currencies[0]['CurrencyCode'] if Related_resource_currencies else 'TMT'

					if user:
						Related_resource_Wish = [wish.to_json_api() for wish in wishes if wish.ResId == resource.ResId]
					else:
						Related_resource_Wish = []

					related_resource_info["Wishlist"] = True if Related_resource_Wish else False
					Related_resources.append(related_resource_info)
				resource_info["Related_resources"] = Related_resources
				# resource_info["Related_resources"] = [resource.to_json_api() for resource in related_resources]
			if fullInfo == True:
				resource_info["UsageStatus"] = dataLangSelector(List_UsageStatus[0]) if List_UsageStatus else []
				resource_info["Barcode"] = List_Barcode if List_Barcode else []
				resource_info["Res_category"] = List_Res_category[0] if List_Res_category else []
				resource_info["Res_price"] = List_Res_price[0] if List_Res_price else []
				resource_info["Currency"] = dataLangSelector(List_Currencies[0]) if List_Currencies else []
				resource_info["Res_total"] = List_Res_total[0] if List_Res_total else []
				resource_info["Rating"] = List_Ratings if List_Ratings else []
			data.append(resource_info)
		except Exception as ex:
			print(f"{datetime.now()} | Resource info utils Exception: {ex}")
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

def apiFeaturedResCat_Resources():
	featured_categories = Res_category.query\
		.filter_by(GCRecord = None)\
		.filter(Res_category.IsMain == True)\
		.order_by(Res_category.ResCatVisibleIndex.asc())\
		.all()

	resource_models = []
	if featured_categories:
		for category in featured_categories:
			featured_resources = Resource.query\
				.filter_by(GCRecord = None)

			if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:
				featured_resources = featured_resources.join(Res_total, Res_total.ResId == Resource.ResId)\
					.filter(and_(
						Res_total.WhId == 1, 
					Res_total.ResTotBalance > 0))

			featured_resources = featured_resources\
				.filter(Resource.ResCatId == category.ResCatId)\
				.order_by(Resource.CreatedDate.desc())\
				.limit(Config.FEATURED_RESOURCE_AMOUNT)\
				.all()

			for resource in featured_resources:
				resource_models.append(resource)
			featured_resources = None

	if resource_models:
		featured_resources = apiResourceInfo(resource_models = resource_models)

	data = []
	if featured_categories:
		for category in featured_categories:
			featured_category = category.to_json_api()
			resources_list = []
			for resource in featured_resources['data']:
				if resource['ResCatId'] == category.ResCatId:
					resources_list.append(resource)
			featured_category['Resources'] = resources_list
			data.append(featured_category)

	res = {
		"status": 1,
		"data": data,
		"total": len(data)
	}
	return res

def UiCartResourceData(product_list,fullInfo=False,showRelated=False):
	res = apiResourceInfo(product_list,fullInfo=fullInfo,showRelated=showRelated)
	data = []
	resources = res['data']
	for resource in resources:
		for product in product_list:
			if (int(resource['ResId'])==int(product['ResId'])):
				try:
					resource["productQty"] = product["productQty"]
				except Exception as ex:
					print(f"{datetime.now()} | Cart Resource Data utils Exception: {ex}")
					resource["productQty"] = 1
		resource["productTotal"]=int(resource["productQty"])*int(resource["ResPriceValue"])
		data.append(resource)
	res = {
		"status": 1,
		"data": data,
		"total": len(data)
	}
	return res

def apiOrderInvInfo(startDate = None,
										endDate = datetime.now(),
										statusId = None,
										single_object = False,
										invoice_list = None,
										rp_acc_user = None,
										DivId = None,
										notDivId = None):
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()

	invoice_filtering = {
		"GCRecord": None
	}
	if statusId:
		invoice_filtering['InvStatId'] = statusId
	if rp_acc_user:
		invoice_filtering['RpAccId'] = rp_acc_user.RpAccId

	order_inv_models = []
	if invoice_list is None:
		order_invoices = Order_inv.query\
			.filter_by(**invoice_filtering)
		if DivId:
			order_invoices = order_invoices.filter_by(DivId = DivId)
		if notDivId:
			order_invoices = order_invoices.filter(Order_inv.DivId != notDivId)

		if startDate:
			# filtering by date
			if (type(startDate) != datetime):
				startDate = dateutil.parser.parse(startDate)
				startDate = datetime.date(startDate)
			if (type(endDate) != datetime):
				endDate = dateutil.parser.parse(endDate)
				endDate = datetime.date(endDate)
			order_invoices = order_invoices\
				.filter(and_(
					extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
					extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
					extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))
			
		order_invoices = order_invoices.order_by(Order_inv.OInvDate.desc()).all()

		for order_inv in order_invoices:
			order_inv_models.append(order_inv)
	else:
		for invoice_index in invoice_list:
			OInvRegNo = invoice_index["OInvRegNo"]
			invoice_filtering["OInvRegNo"] = OInvRegNo
			order_inv = Order_inv.query\
				.filter_by(**invoice_filtering).first()
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
				rp_acc_user = Rp_acc.query\
					.filter_by(GCRecord = None, RpAccId = order_inv.RpAccId)\
					.first()
				rpAccData = apiRpAccData(dbModel=rp_acc_user)
			rp_acc_user = None
			order_inv_info['Rp_acc'] = rpAccData['data']

			order_inv_lines = []
			for order_inv_line in order_inv.Order_inv_line:
				if order_inv_line.GCRecord == None:
					this_order_inv_line = order_inv_line.to_json_api()
					try:
						resource = Resource.query\
							.filter_by(GCRecord = None, ResId = order_inv_line.ResId)\
							.first()
						resource_json = apiResourceInfo(resource_models=[resource],single_object=True)
						this_order_inv_line['Resource'] = resource_json['data']
					except Exception as ex:
						print(f"{datetime.now()} | Order_inv_line info utils Exception: {ex}")
						this_order_inv_line['Resource'] = []
					order_inv_lines.append(this_order_inv_line)
			
			order_inv_info['Order_inv_lines'] = order_inv_lines
			# order_inv_info['Order_inv_lines'] = [order_inv_line.to_json_api() for order_inv_line in order_inv.Order_inv_line if order_inv_line.GCRecord == None]
			data.append(order_inv_info)
		except Exception as ex:
			print(f"{datetime.now()} | Order_inv info utils Exception: {ex}")
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

def apiInvInfo(startDate = None,
							endDate = datetime.now(),
							statusId = None,
							single_object = False,
							invoice_list = None,
							rp_acc_user = None,
							DivId = None,
							notDivId = None):
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()

	invoice_filtering = {
		"GCRecord": None
	}
	if statusId:
		invoice_filtering['InvStatId'] = statusId
	if rp_acc_user:
		invoice_filtering['RpAccId'] = rp_acc_user.RpAccId

	inv_models = []
	if invoice_list is None:
		invoices = Invoice.query.filter_by(**invoice_filtering)

		if DivId:
			invoices = invoices.filter_by(DivId = DivId)
		if notDivId:
			invoices = invoices.filter(Invoice.DivId != notDivId)

		if startDate:
			# filtering by date
			if (type(startDate) != datetime):
				startDate = dateutil.parser.parse(startDate)
				startDate = datetime.date(startDate)
			if (type(endDate) != datetime):
				endDate = dateutil.parser.parse(endDate)
				endDate = datetime.date(endDate)
			invoices = invoices\
				.filter(and_(
					extract('year',Invoice.InvDate).between(startDate.year,endDate.year),\
					extract('month',Invoice.InvDate).between(startDate.month,endDate.month),\
					extract('day',Invoice.InvDate).between(startDate.day,endDate.day)))
			
		invoices = invoices.order_by(Invoice.InvDate.desc()).all()

		for invoice in invoices:
			inv_models.append(invoice)
	else:
		for invoice_index in invoice_list:
			InvRegNo = invoice_index["InvRegNo"]
			invoice_filtering["InvRegNo"] = InvRegNo
			invoice = Invoice.query\
				.filter_by(**invoice_filtering).first()
			if invoice:
				inv_models.append(invoice)

	data = []
	fails = []
	for invoice in inv_models:
		try:
			inv_info = invoice.to_json_api()

			inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == invoice.InvStatId]
			inv_status = dataLangSelector(inv_status_list[0])
			inv_info['InvStatName'] = inv_status['InvStatName']

			if rp_acc_user:
				rpAccData = apiRpAccData(dbModel=rp_acc_user)
			else:
				rp_acc_user = Rp_acc.query\
					.filter_by(GCRecord = None, RpAccId = invoice.RpAccId)\
					.first()
				rpAccData = apiRpAccData(dbModel=rp_acc_user)
			rp_acc_user = None
			inv_info['Rp_acc'] = rpAccData['data']

			inv_lines = []
			for inv_line in invoice.Inv_line:
				if inv_line.GCRecord == None:
					this_inv_line = inv_line.to_json_api()
					try:
						resource = Resource.query\
							.filter_by(GCRecord = None, ResId = inv_line.ResId)\
							.first()
						resource_json = apiResourceInfo(resource_models=[resource],single_object=True)
						this_inv_line['Resource'] = resource_json['data']
					except Exception as ex:
						print(f"{datetime.now()} | Invoice_line info utils Exception: {ex}")
						this_inv_line['Resource'] = []
					inv_lines.append(this_inv_line)
			
			inv_info['Inv_lines'] = inv_lines
			data.append(inv_info)
		except Exception as ex:
			print(f"{datetime.now()} | Invoice info utils Exception: {ex}")
			fails.append(invoice.to_json_api())
	
	status = checkApiResponseStatus(data,fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		if len(fails) == 1:
			fails = fails[0]
	res = {
			"message": "Invoice",
			"data": data,
			"fails": fails,
			"total": len(data),
			"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]
	return res