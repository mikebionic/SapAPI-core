from sqlalchemy import and_
from flask import jsonify,request,abort,make_response

# auth and validation
from flask_login import current_user,login_required
from main_pack.base.apiMethods import checkApiResponseStatus,fileToURL
# / auth and validation /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# db models 
from main_pack.models_test.commerce.models import (Resource,
                                              Barcode,
                                              Res_category,
                                              Res_price,
                                              Res_total,
                                              Res_unit,
                                              Res_color,
                                              Res_size,
																							Wish,
																							Rating)
from main_pack.models_test.commerce.models import (Color,
                                              Size,
                                              Brand,
                                              Unit,
                                              Usage_status)
from main_pack.models_test.base.models import (Image,
																					Currency)
# / db models /

# isDeleted shows deleted resources with GCRecord != None
# isInactive shows active resources with UsageStatusId = 1
# fullInfo shows microframework full info with Foreign tables
# single_object returns one resource in "data" instead of list 
def apiResourceInfo(resource_list=None,single_object=False,isDeleted=False,isInactive=False,fullInfo=False,user=None):
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
	currencies = Currency.query\
		.filter(Currency.GCRecord=='' or Currency.GCRecord==None).all()
	ratings = Rating.query\
		.filter(Rating.GCRecord=='' or Rating.GCRecord==None).all()

	if current_user.is_authenticated:
		user=current_user
	if user:
		RpAccId = user.RpAccId
		wishes = Wish.query\
			.filter(and_(Wish.GCRecord=='' or Wish.GCRecord==None),\
				Wish.RpAccId==RpAccId)\
			.all()
	
	resource_models = []
	if resource_list is None:
		if isDeleted==True:
			if isInactive==True:
				resources = Resource.query.all()
			else:
				resources = Resource.query\
					.filter(Resource.UsageStatusId==1).all()
		else:
			if isInactive==True:
				resources = Resource.query\
					.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()	
			else:
				resources = Resource.query\
					.filter(and_(\
						(Resource.GCRecord=='' or Resource.GCRecord==None),\
						Resource.UsageStatusId==1)).all()
		for resource in resources:
			resource_models.append(resource)

	else:
		for resource_index in resource_list:
			ResId = int(resource_index["ResId"])
			if isDeleted==True:
				if isInactive==True:
					resource = Resource.query\
						.filter((Resource.ResId==ResId)).first()
				else:
					resource = Resource.query\
						.filter(and_(\
							(Resource.ResId==ResId),\
							Resource.UsageStatusId==1)).first()
			else:
				if isInactive==True:
					resource = Resource.query\
						.filter(and_(\
							(Resource.ResId==ResId),\
							(Resource.GCRecord=='' or Resource.GCRecord==None))).first()	
				else:
					resource = Resource.query\
						.filter(and_(\
							(Resource.ResId==ResId),\
							(Resource.GCRecord=='' or Resource.GCRecord==None),\
							Resource.UsageStatusId==1)).first()
			if resource:
				resource_models.append(resource)
		
	data = []
	fails = []
	for resource in resource_models:
		try:
			resource_info = resource.to_json_api()

			List_Barcode = [barcode.to_json_api() for barcode in barcodes if barcode.ResId==resource.ResId]
			List_Res_category = [category.to_json_api() for category in categories if category.ResCatId==resource.ResCatId]
			List_Res_price = [res_price.to_json_api() for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
			List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId==List_Res_price[0]['CurrencyId']]
			List_Res_total = [res_total.to_json_api() for res_total in res_totals if res_total.ResId==resource.ResId]
			List_Images = [image.to_json_api() for image in images if image.ResId==resource.ResId]
			List_Colors = [color.to_json_api() for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
			List_Sizes = [size.to_json_api() for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
			List_Brands = [brand.to_json_api() for brand in brands if brand.BrandId==resource.BrandId]
			List_UsageStatus = [usage_status.to_json_api() for usage_status in usage_statuses if usage_status.UsageStatusId==resource.UsageStatusId]
			List_Units = [unit.to_json_api() for unit in units if unit.UnitId==resource.UnitId]
			List_Ratings = [rating.to_json_api() for rating in ratings if rating.ResId==resource.ResId]
			if user:
				List_Wish = [wish.to_json_api() for wish in wishes if wish.ResId==resource.ResId]
			else:
				List_Wish = []

			resource_info["BarcodeVal"] = List_Barcode[0]['BarcodeVal'] if List_Barcode else ''
			resource_info["ResCatName"] = List_Res_category[0]['ResCatName'] if List_Res_category else ''
			resource_info["ResPriceValue"] = List_Res_price[0]['ResPriceValue'] if List_Res_price else ''
			resource_info["CurrencyCode"] = List_Currencies[0]['CurrencyCode'] if List_Currencies else 'TMT'
			resource_info["ResTotBalance"] = List_Res_total[0]['ResTotBalance'] if List_Res_total else ''
			resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
			resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
			resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''
			resource_info["Images"] = List_Images if List_Images else []
			resource_info["Colors"] = List_Colors if List_Colors else []
			resource_info["Sizes"] = List_Sizes if List_Sizes else []
			resource_info["Brand"] = List_Brands[0] if List_Brands else []
			resource_info["Unit"] = dataLangSelector(List_Units[0]) if List_Units else []
			resource_info["RtRatingValue"] = List_Ratings[0]['RtRatingValue'] if List_Ratings else 0.0
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
	if single_object==True:
		if len(data)==1:
			data = data[0]
		if len(fails)==1:
			fails = fails[0]
	res = {
			"message": "Resources",
			"data": data,
			"fails": fails,
			"total": len(data),
			"fail_total": len(fails)
	}
	for e in status:
		res[e]=status[e]
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