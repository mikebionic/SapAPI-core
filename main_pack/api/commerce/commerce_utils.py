# -*- coding: utf-8 -*-
from flask import session

from main_pack.config import Config
from main_pack import db, cache

# functions and methods
from main_pack.base.apiMethods import checkApiResponseStatus, fileToURL
# functions and methods

# auth and validation
from flask_login import current_user
# / auth and validation /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.priceMethods import calculatePriceByGroup, price_currency_conversion, configureDecimal
# / functions and methods /

# db models
# from main_pack.models import Company, Division, Warehouse, Image, Res_translation
from main_pack.models import (
	Resource,
	Res_price,
	Res_price_group,
	Res_total,
	Res_category,
	Wish,
	Rating,
	Exc_rate)
from main_pack.models import (
	Res_color,
	Res_size,
	Brand,
)
from main_pack.models import Currency
# / db models /

# orders and db methods
from main_pack.models import (
	Order_inv,
	Order_inv_line,
	Invoice,
	Inv_status)
from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models import Rp_acc, User
from main_pack.api.users.utils import apiRpAccData, apiUsersData
# / Rp_acc db Model and methods /

# datetime, date-parser
import dateutil.parser
from datetime import datetime, timedelta
# / datetime, date-parser /

from main_pack.base.invoiceMethods import getInvStatusUi


def collect_categories_query(
	DivId = None,
	notDivId = None,
	avoidQtyCheckup = 0,
	showNullResourceCategory = 0,
	IsMain = False):

	Res_Total_subquery = db.session.query(
		Res_total.ResId,
		db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
		db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))

	if DivId:
		Res_Total_subquery = Res_Total_subquery\
			.filter(Res_total.DivId == DivId)

	Res_Total_subquery = Res_Total_subquery\
		.group_by(Res_total.ResId)\
		.subquery()

	categories_query = Res_category.query\
		.filter_by(GCRecord = None)\
		.options(
			joinedload(Res_category.subcategory)\
				.options(
					joinedload(Res_category.Resource)))

	if Config.HIDE_UNDER_ZERO_VISIBLE_CATEGORIES:
		categories_query = categories_query\
			.filter(Res_category.ResCatVisibleIndex >= 0)

	if showNullResourceCategory:
		categories_query = categories_query\
			.outerjoin(Resource, Resource.ResCatId == Res_category.ResCatId)\

	else:
		categories_query = categories_query\
			.join(Resource, Resource.ResCatId == Res_category.ResCatId)\

	categories_query = categories_query\
		.filter(Resource.GCRecord == None)\
		.outerjoin(Res_Total_subquery, Res_Total_subquery.c.ResId == Resource.ResId)

	if IsMain == True:
		categories_query = categories_query\
			.filter(Res_category.IsMain == True)

	if avoidQtyCheckup == 0:
		if (not Config.SHOW_NEGATIVE_WH_QTY_RESOURCE and not showNullResourceCategory):
			categories_query = categories_query\
				.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

	# if DivId:
	# 	categories_query = categories_query.filter(Resource.DivId == DivId)
	if notDivId:
		categories_query = categories_query.filter(Resource.DivId != notDivId)

	categories_query = categories_query.order_by(Res_category.ResCatVisibleIndex.asc())
	return categories_query


def collect_resources_query(
	showInactive = False,
	showLatest = False,
	showRated = False,
	showMain = False,
	limit_by = None,
	avoidQtyCheckup = 0,
	showNullPrice = False,
	DivId = None,
	notDivId = None):
	resource_filtering = {
		"GCRecord": None,
	}
	if showInactive == False:
		resource_filtering["UsageStatusId"] = 1

	Res_Total_subquery = db.session.query(
		Res_total.ResId,
		db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
		db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))

	if DivId:
		Res_Total_subquery = Res_Total_subquery\
			.filter(Res_total.DivId == DivId)

	Res_Total_subquery = Res_Total_subquery\
		.group_by(Res_total.ResId)\
		.subquery()

	resource_query = db.session.query(
		Resource,
		Res_Total_subquery.c.ResTotBalance_sum,
		Res_Total_subquery.c.ResPendingTotalAmount_sum)\
	.filter_by(**resource_filtering)\
	.outerjoin(Res_Total_subquery, Resource.ResId == Res_Total_subquery.c.ResId)

	if avoidQtyCheckup == 0:
		if not Config.SHOW_NEGATIVE_WH_QTY_RESOURCE:
			resource_query = resource_query\
				.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

	if showMain:
		resource_query = resource_query\
			.filter(Resource.IsMain > 0)

	if showNullPrice == False:
		resource_query = resource_query\
			.join(Res_price, Res_price.ResId == Resource.ResId)\
			.filter(and_(
				Res_price.ResPriceTypeId == 2,
				Res_price.ResPriceValue > 0))\

	category_joined = False

	if Config.HIDE_UNDER_ZERO_VISIBLE_CATEGORIES:
		resource_query = resource_query\
			.join(Res_category, Res_category.ResCatId == Resource.ResCatId)\
			.filter(Res_category.ResCatVisibleIndex >= 0)
		category_joined = True

	if showRated == True:
		if not category_joined:
			resource_query = resource_query\
				.join(Res_category, Res_category.ResCatId == Resource.ResCatId)

		resource_query = resource_query\
			.filter(Res_category.IsMain == True)\
			.outerjoin(Rating, Rating.ResId == Resource.ResId)\
			.filter(Rating.RtRatingValue >= Config.SMALLEST_RATING_VALUE_SHOW)\
			.order_by(Rating.RtRatingValue.asc())\
			.limit(Config.RESOURCE_MAIN_PAGE_SHOW_QTY)

	if showLatest == True:
		resource_query = resource_query\
			.order_by(Resource.CreatedDate.desc())\
			.limit(Config.RESOURCE_MAIN_PAGE_SHOW_QTY)

	if limit_by:
		resource_query = resource_query.limit(limit_by)

	if notDivId:
		resource_query = resource_query.filter(Resource.DivId != notDivId)

	return resource_query


# showInactive shows active resources with UsageStatusId = 1
# fullInfo shows microframework full info with Foreign tables
# single_object returns one resource in "data" instead of list
# showRated gives you latest rated resources
# showLatest gives you latest resources by datetime
def apiResourceInfo(
	resource_list = None,
	single_object = False,
	showInactive = False,
	fullInfo = False,
	user = None,
	ResPriceGroupId = None,
	resource_models = None,
	resource_query = None,
	showRelated = False,
	showLatest = False,
	showRated = False,
	showMain = None,
	avoidQtyCheckup = 0,
	showNullPrice = False,
	DivId = None,
	notDivId = None,
	currency_code = None,
	language_code = None,
	order_by_visible_index = False,
	limit_by = None,
	showRatings = 0,
	showImage = 1,
	showLastVendor = 0,
	showBoughtPrice = 0,
):

	currencies = Currency.query.filter_by(GCRecord = None).all()
	res_price_groups = Res_price_group.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	# return wishlist info for authenticated user
	if current_user.is_authenticated:
		user = current_user
	if user:
		RpAccId = user.RpAccId
		# wishes = [wish for wish in user.Wish if wish.GCRecord == None]
		wishes = Wish.query\
			.filter_by(GCRecord = None, RpAccId = RpAccId)\
			.all()

	# ResPriceGroupId assignment and validation
	if not ResPriceGroupId:
		ResPriceGroupId = Config.DEFAULT_RES_PRICE_GROUP_ID
		try:
			if "ResPriceGroupId" in session:
				if session["ResPriceGroupId"]:
					ResPriceGroupId = session["ResPriceGroupId"]

			elif current_user.is_authenticated:
				if current_user.ResPriceGroupId:
					ResPriceGroupId = current_user.ResPriceGroupId

		except Exception as ex:
			print(f"{datetime.now()} | resource_info api ResPriceGroupId exception: {ex}")

	if not currency_code:
		if "currency_code" in session:
			currency_code = session["currency_code"] if session["currency_code"] else None

	if not language_code:
		if "language" in session:
			language_code = session["language"] if session["language"] else None

	if not resource_models:
		resource_models = []
		# if list with "ResId" is not provided, return all resources
		if resource_list is None:
			if resource_query is None:
				resource_query = collect_resources_query(
					showInactive = showInactive,
					showLatest = showLatest,
					showRated = showRated,
					showMain = showMain,
					avoidQtyCheckup = avoidQtyCheckup,
					showNullPrice = showNullPrice,
					DivId = DivId,
					notDivId = notDivId)

			resources = resource_query.options(
				joinedload(Resource.Barcode),
				joinedload(Resource.Rating),
				joinedload(Resource.Res_price),
				joinedload(Resource.Res_total),
				joinedload(Resource.res_category),
				joinedload(Resource.unit),
				joinedload(Resource.brand),
				joinedload(Resource.usage_status),
				joinedload(Resource.Res_discount_SaleResId))
			
			if showImage:
				resources = resources.options(joinedload(Resource.Image))

			if showLastVendor:
				resources = resources.options(joinedload(Resource.last_vendor))

			if Config.SHOW_RES_TRANSLATIONS:
				resources = resources.options(joinedload(Resource.Res_translation))

			if order_by_visible_index:
				resources = resources.order_by(Resource.ResVisibleIndex.asc())

			if limit_by:
				resources = resources.limit(limit_by)

			if fullInfo == True:
				# !!! TODO: Res_color and color joins could be implemented on class level
				resources = resources.options(
					joinedload(Resource.Res_color)\
						.options(joinedload(Res_color.color)),
					joinedload(Resource.Res_size)\
						.options(joinedload(Res_size.size))
					)

			resource_models = [resource for resource in resources if resources]

		else:
			res_id_list = [int(resource_index["ResId"]) for resource_index in resource_list if resource_index]
			resource_filtering = {"GCRecord": None}
			if not showInactive:
				resource_filtering["UsageStatusId"] = 1

			Res_Total_subquery = db.session.query(
				Res_total.ResId,
				db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
				db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))

			if DivId:
				Res_Total_subquery = Res_Total_subquery\
					.filter(Res_total.DivId == DivId)

			Res_Total_subquery = Res_Total_subquery\
				.group_by(Res_total.ResId)\
				.subquery()

			resource_query = db.session.query(
				Resource,
				Res_Total_subquery.c.ResTotBalance_sum,
				Res_Total_subquery.c.ResPendingTotalAmount_sum)\
			.filter_by(**resource_filtering)\
			.filter(Resource.ResId.in_(res_id_list))\
			.outerjoin(Res_Total_subquery, Resource.ResId == Res_Total_subquery.c.ResId)

			if avoidQtyCheckup == 0:
				if not Config.SHOW_NEGATIVE_WH_QTY_RESOURCE:
					resource_query = resource_query\
						.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

			if showNullPrice == False:
				resource_query = resource_query\
					.join(Res_price, Res_price.ResId == Resource.ResId)\
					.filter(Res_price.ResPriceValue > 0)

			resource_query = resource_query.options(
				joinedload(Resource.Barcode),
				joinedload(Resource.Res_price),
				joinedload(Resource.Res_total),
				joinedload(Resource.res_category),
				joinedload(Resource.unit),
				joinedload(Resource.brand).options(joinedload(Brand.Image)),
				joinedload(Resource.usage_status),
				joinedload(Resource.Res_discount_SaleResId))

			if showImage:
				resource_query = resource_query.options(joinedload(Resource.Image))

			if showLastVendor:
				resource_query = resource_query.options(joinedload(Resource.last_vendor))

			if fullInfo:
				resource_query = resource_query.options(
					joinedload(Resource.Res_color)\
						.options(joinedload(Res_color.color)),
					joinedload(Resource.Res_size)\
						.options(joinedload(Res_size.size)),
					joinedload(Resource.Rating)\
						.options(
							joinedload(Rating.user).options(joinedload(User.Image)),
							joinedload(Rating.rp_acc).options(joinedload(Rp_acc.Image))
						)
					)

			elif fullInfo == False:
				resource_query = resource_query.options(joinedload(Resource.Rating))

			resource_models = resource_query.all()

	data, fails = [], []

	for resource_query in resource_models:
		try:
			query_resource = resource_query.Resource
			resource_info = query_resource.to_json_api()
			Brands_info = {}
			if query_resource.brand:
				Brands_info = query_resource.brand.to_json_api()
				Brands_info["Images"] = [image.to_json_api() for image in query_resource.brand.Image if not image.GCRecord]
			UsageStatus_info = query_resource.usage_status.to_json_api() if query_resource.usage_status else None
			Units_info = query_resource.unit.to_json_api() if query_resource.unit else None
			Res_category_info = query_resource.res_category.to_json_api() if query_resource.res_category else None

			List_Barcode = [barcode.to_json_api() for barcode in query_resource.Barcode if not barcode.GCRecord]

			List_Res_price = calculatePriceByGroup(
				ResPriceGroupId = ResPriceGroupId,
				Res_price_dbModels = query_resource.Res_price,
				Res_pice_group_dbModels = res_price_groups)
			
			if showBoughtPrice:
				List_Res_price_sale = calculatePriceByGroup(
					ResPriceGroupId = ResPriceGroupId,
					Res_price_dbModels = query_resource.Res_price,
					Res_pice_group_dbModels = res_price_groups,
					ResPriceTypeId=1
				)

			if not List_Res_price:
				raise Exception

			try:
				List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == List_Res_price[0]["CurrencyId"]]
			except:
				List_Currencies = []

			this_priceValue = List_Res_price[0]["ResPriceValue"] if List_Res_price else 0.0
			if showBoughtPrice:
				this_priceValue_sale = List_Res_price_sale[0]["ResPriceValue"] if List_Res_price_sale else 0.0
				
			this_currencyCode = List_Currencies[0]["CurrencyCode"] if List_Currencies else Config.MAIN_CURRENCY_CODE
			resource_info["RealPrice"] = this_priceValue
			resource_info["DiscValue"] = None
			resource_info["DiscType"] = None

			if query_resource.Res_discount_SaleResId:
				applying_disc = query_resource.Res_discount_SaleResId[-1]
				if applying_disc.DiscTypeId == 1 and applying_disc.ResDiscIsActive:
					resource_info["DiscValue"] = applying_disc.DiscValue
					resource_info["DiscType"] = "%"
					this_priceValue = float(configureDecimal(float(this_priceValue) - (float(this_priceValue) * float(applying_disc.DiscValue) / 100)))

			price_data = price_currency_conversion(
				priceValue = this_priceValue,
				from_currency = this_currencyCode,
				to_currency = currency_code,
				currencies_dbModel = currencies,
				exc_rates_dbModel = exc_rates)
			
			if showBoughtPrice:
				price_data_sale = price_currency_conversion(
					priceValue = this_priceValue_sale,
					from_currency = this_currencyCode,
					to_currency = currency_code,
					currencies_dbModel = currencies,
					exc_rates_dbModel = exc_rates)

			List_Res_total = [res_total.to_json_api() for res_total in query_resource.Res_total if not res_total.GCRecord and res_total.WhId == 1]

			List_Images = []
			if showImage:
				List_Images = [image.to_json_api() for image in query_resource.Image if not image.GCRecord]
				# Sorting list by Modified date
				List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))


			if showRatings or fullInfo:
				List_Ratings = []
				for rating in query_resource.Rating:
					try:
						if (Config.SHOW_ONLY_VALIDATED_RATING and not rating.RtValidated):
							raise Exception

						Rating_info = rating.to_json_api()

						if rating.UId:
							userData = apiUsersData(dbModel = rating.user, rpAccInfo = False, additionalInfo = False) if not rating.user.GCRecord else None
							Rating_info["User"] = userData["data"] if userData else {}

						if rating.RpAccId:
							rpAccData = apiRpAccData(dbModel = rating.rp_acc, userInfo = False, additionalInfo = False) if not rating.rp_acc.GCRecord else None
							Rating_info["Rp_acc"] = rpAccData["data"] if rpAccData else {}

						List_Ratings.append(Rating_info)

					except:
						pass

			else:
				if Config.SHOW_ONLY_VALIDATED_RATING:
					List_Ratings = [rating.to_json_api() for rating in query_resource.Rating if not rating.GCRecord and rating.RtValidated]
				else:
					List_Ratings = [rating.to_json_api() for rating in query_resource.Rating if not rating.GCRecord]
			if user:
				List_Wish = [wish.to_json_api() for wish in wishes if wish.ResId == query_resource.ResId]
			else:
				List_Wish = []

			resource_info["BarcodeVal"] = List_Barcode[0]["BarcodeVal"] if List_Barcode else ""
			resource_info["ResCatName"] = Res_category_info["ResCatName"] if Res_category_info else ""
			resource_info["CategoryIcon"] = Res_category_info["ResCatIconFilePath"] if Res_category_info else ""
			resource_info["ResPriceValue"] = price_data["ResPriceValue"]
			resource_info["CurrencyCode"] = price_data["CurrencyCode"]
			resource_info["CurrencySymbol"] = price_data["CurrencySymbol"]
			if showBoughtPrice:
				resource_info["SaleResPriceValue"] = price_data_sale["ResPriceValue"]
			resource_info["ResTotBalance"] = 9999 if Config.SET_UNLIMITED_RESOURCE_QTY == 1 else resource_query.ResTotBalance_sum if resource_query.ResTotBalance_sum else 0.0
			resource_info["ResPendingTotalAmount"] = 9999 if Config.SET_UNLIMITED_RESOURCE_QTY == 1 else resource_query.ResPendingTotalAmount_sum if resource_query.ResPendingTotalAmount_sum else 0.0

			if showImage:
				resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
				resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
				resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
				resource_info["Images"] = List_Images if List_Images else []

			if showLastVendor:
				resource_info["LastVendorName"] = query_resource.last_vendor.RpAccUName if query_resource.last_vendor else ""

			if Config.SHOW_RES_TRANSLATIONS:
				if query_resource.Res_translation and language_code:
					for res_transl in query_resource.Res_translation:
						if language_code in res_transl.language.LangName:
							resource_info["ResName"] = res_transl.ResName
							resource_info["ResDesc"] = res_transl.ResDesc

			if Brands_info:
				resource_info["BrandName"] = Brands_info["BrandName"] if Brands_info else ""
				resource_info["BrandIcon"] = Brands_info["Images"][0]["FilePath"] if Brands_info["Images"] else ""

			resource_info["UnitName"] = dataLangSelector(Units_info)["UnitName"] if Units_info else ""
			resource_info["UsageStatusName"] = dataLangSelector(UsageStatus_info)["UsageStatusName"] if UsageStatus_info else ""

			rating_values = [rating["RtRatingValue"] for rating in List_Ratings if List_Ratings]
			try:
				average_rating = sum(rating_values) / len(rating_values)
				average_rating = round(average_rating,2)
			except Exception as ex:
				average_rating = 0.0

			resource_info["RtRatingValue"] = average_rating
			resource_info["Wishlist"] = True if List_Wish else False
			resource_info["New"] = True if query_resource.CreatedDate >= datetime.today() - timedelta(days=Config.COMMERCE_RESOURCE_NEWNESS_DAYS) else False
			if showRelated == True:
				related_resources = Resource.query\
					.filter_by(GCRecord = None, ResCatId = query_resource.ResCatId)\
					.filter(Resource.ResId != query_resource.ResId)\
					.join(Res_total, Res_total.ResId == Resource.ResId)\
					.filter(and_(
						Res_total.WhId == 1,
						Res_total.ResTotBalance > 0))\
					.outerjoin(Rating, Rating.ResId == Resource.ResId)\
					.order_by(Rating.RtRatingValue.asc())\
					.limit(Config.TOP_RATED_RESOURCES_AMOUNT+1)\

				related_resources = related_resources\
					.options(
						joinedload(Resource.res_category),
						joinedload(Resource.Image))

				Related_resources = []
				for resource in related_resources:
					try:
						related_resource_info = resource.to_json_api()
						Related_resource_Images = [image.to_json_api() for image in resource.Image if not image.GCRecord]
						related_resource_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=Related_resource_Images[-1]["FileName"]) if Related_resource_Images else ""
						related_resource_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=Related_resource_Images[-1]["FileName"]) if Related_resource_Images else ""
						related_resource_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=Related_resource_Images[-1]["FileName"]) if Related_resource_Images else ""

						Related_Res_category_info = resource.res_category.to_json_api() if resource.res_category else None
						Related_resource_price = [res_price.to_json_api() for res_price in resource.Res_price if res_price.ResPriceTypeId == 2 and not res_price.GCRecord]

						Related_resource_price = calculatePriceByGroup(
							ResPriceGroupId = ResPriceGroupId,
							Res_price_dbModels = resource.Res_price,
							Res_pice_group_dbModels = res_price_groups)

						if not Related_resource_price:
							raise Exception

						try:
							Related_resource_currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == Related_resource_price[0]["CurrencyId"]]
						except:
							Related_resource_currencies = []

						this_priceValue = Related_resource_price[0]["ResPriceValue"] if Related_resource_price else 0.0
						this_currencyCode = Related_resource_currencies[0]["CurrencyCode"] if Related_resource_currencies else Config.MAIN_CURRENCY_CODE
						related_resource_info["RealPrice"] = this_priceValue

						related_resource_info["DiscValue"] = None
						related_resource_info["DiscType"] = None
						if resource.Res_discount_SaleResId:
							applying_disc = resource.Res_discount_SaleResId[-1]
							if applying_disc.DiscTypeId == 1 and applying_disc.ResDiscIsActive:
								related_resource_info["DiscValue"] = applying_disc.DiscValue
								related_resource_info["DiscType"] = "%"
								this_priceValue = float(configureDecimal(float(this_priceValue) - (float(this_priceValue) * float(applying_disc.DiscValue) / 100)))

						Related_resource_price_data = price_currency_conversion(
							priceValue = this_priceValue,
							from_currency = this_currencyCode,
							to_currency = currency_code,
							currencies_dbModel = currencies,
							exc_rates_dbModel = exc_rates)

						related_resource_info["ResCatName"] = Related_Res_category_info["ResCatName"] if Related_Res_category_info else ""
						related_resource_info["ResPriceValue"] = Related_resource_price_data["ResPriceValue"]
						related_resource_info["CurrencyCode"] = Related_resource_price_data["CurrencyCode"]
						related_resource_info["CurrencySymbol"] = Related_resource_price_data["CurrencySymbol"]

						if user:
							Related_resource_Wish = [wish.to_json_api() for wish in wishes if wish.ResId == resource.ResId]
						else:
							Related_resource_Wish = []

						related_resource_info["Wishlist"] = True if Related_resource_Wish else False
						Related_resources.append(related_resource_info)

					except Exception as ex:
						print(f"{datetime.now()} | Related resource info utils Exception: {ex}")

					resource_info["Related_resources"] = Related_resources

			if fullInfo:
				List_Colors = [res_color.color.to_json_api() for res_color in query_resource.Res_color if not res_color.GCRecord if not res_color.color.GCRecord]
				List_Sizes = [res_size.size.to_json_api() for res_size in query_resource.Res_size if not res_size.GCRecord if not res_size.size.GCRecord]
				resource_info["Colors"] = List_Colors if List_Colors else []
				resource_info["Sizes"] = List_Sizes if List_Sizes else []
				resource_info["Barcode"] = List_Barcode if List_Barcode else []
				resource_info["Brand"] = Brands_info if Brands_info else {}
				resource_info["Res_category"] = Res_category_info if Res_category_info else {}
				resource_info["Res_price"] = List_Res_price[0] if List_Res_price else {}
				resource_info["Res_total"] = List_Res_total[0] if List_Res_total else {}
				resource_info["UsageStatus"] = dataLangSelector(UsageStatus_info) if UsageStatus_info else {}
				resource_info["Currency"] = dataLangSelector(List_Currencies[0]) if List_Currencies else {}
				resource_info["Unit"] = dataLangSelector(Units_info) if Units_info else {}

			if showRatings or fullInfo:
				resource_info["Rating"] = List_Ratings if List_Ratings else []

			data.append(resource_info)

		except Exception as ex:
			print(f"{datetime.now()} | Resource info utils Exception: {ex}")
			fails.append(query_resource.to_json_api())

	status = checkApiResponseStatus(data,fails)
	total = len(data)
	fail_total = len(fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		elif not data:
			data = {}
		total = 1 if data else 0

		if len(fails) == 1:
			fails = fails[0]
		elif not data:
			data = {}
		fail_total = 1 if data else 0

	res = {
			"message": "Resources",
			"data": data,
			"fails": fails,
			"total": total,
			"fail_total": fail_total
	}
	for e in status:
		res[e] = status[e]
	return res


@cache.cached(Config.DB_CACHE_TIME, key_prefix="featured_categories")
def get_FeaturedResCategory_list(DivId = None):
	featured_categories = collect_categories_query(
		IsMain = True,
		showNullResourceCategory = Config.SHOW_NULL_RESOURCE_CATEGORY,
		DivId = DivId
	)

	featured_categories = featured_categories\
		.all()

	return featured_categories


def apiFeaturedResCat_Resources(DivId = None):
	featured_categories = get_FeaturedResCategory_list(DivId)
	if featured_categories:
		featured_resources_query = collect_resources_query(DivId = DivId)

		categories_data = {}
		for category in featured_categories:
			this_cat_categories = []
			this_cat_categories.append(category.ResCatId)
			if category.subcategory:
				for subcategory in category.subcategory:
					this_cat_categories.append(subcategory.ResCatId)

			this_cat_categories = list(set(this_cat_categories))
			this_cat_categories = [ResCatId for ResCatId in this_cat_categories]
			categories_data[str(category.ResCatId)] = {}
			categories_data[str(category.ResCatId)]["category_ids"] = this_cat_categories
			categories_data[str(category.ResCatId)]["data"] = category.to_json_api()

		for category in featured_categories:
			resource_query = featured_resources_query\
				.filter(Resource.ResCatId.in_(categories_data[str(category.ResCatId)]["category_ids"]))\
				.order_by(Resource.CreatedDate.desc())\
				.limit(Config.FEATURED_RESOURCE_AMOUNT)

			resources = apiResourceInfo(resource_query = resource_query)
			categories_data[str(category.ResCatId)]["data"]["Resources"] = resources["data"]

	data = []
	for category in featured_categories:
		data.append(categories_data[str(category.ResCatId)]["data"])

	res = {
		"status": 1 if len(data) > 0 else 0,
		"data": data,
		"total": len(data)
	}
	return res


def UiCartResourceData(
	product_list,
	fullInfo = False,
	showRelated = False,
	DivId = None
):
	res = apiResourceInfo(
		product_list,
		fullInfo = fullInfo,
		showRelated = showRelated,
		DivId = DivId)
	data = []
	resources = res["data"]
	for resource in resources:
		for product in product_list:
			if (int(resource["ResId"]) == int(product["ResId"])):
				try:
					resource["productQty"] = product["productQty"]
				except Exception as ex:
					print(f"{datetime.now()} | Cart Resource Data utils Exception: {ex}")
					resource["productQty"] = 1
		resource["productTotal"] = round((float(resource["productQty"]) * float(resource["ResPriceValue"])), 2)
		data.append(resource)
	res = {
		"status": 1 if len(data) > 0 else 0,
		"data": data,
		"total": len(data)
	}
	return res


# !!! TODO: Should be optimized
def apiOrderInvInfo(
	startDate = None,
	endDate = datetime.now(),
	statusId = None,
	single_object = False,
	invoice_list = None,
	invoice_models = None,
	invoices_only = False,
	show_inv_line_resource = False,
	rp_acc_user = None,
	DivId = None,
	notDivId = None,
	currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE,
	limit_by = None,
	UId = None,
	RpAccId = None,
	UGuid = None,
	RpAccGuid = None,
):

	currencies = Currency.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	if not invoice_models:
		invoice_filtering = {
			"GCRecord": None
		}
		if statusId:
			invoice_filtering["InvStatId"] = statusId
		if rp_acc_user:
			invoice_filtering["RpAccId"] = rp_acc_user.RpAccId

		if UId:
			invoice_filtering["UId"] = UId
		if RpAccId:
			invoice_filtering["RpAccId"] = RpAccId

		if UGuid:
			this_user = User.query.filter_by(UGuid = UGuid).first()
			if this_user:
				invoice_filtering["UId"] = this_user.UId
		if RpAccGuid:
			tihs_rp_acc = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
			if tihs_rp_acc:
				invoice_filtering["RpAccId"] = tihs_rp_acc.RpAccId

		invoice_models = []
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

			order_invoices = order_invoices\
				.order_by(Order_inv.OInvDate.desc())\
				.options(
					joinedload(Order_inv.rp_acc),
					joinedload(Order_inv.inv_status),
					joinedload(Order_inv.company),
					joinedload(Order_inv.warehouse),
					joinedload(Order_inv.division),
					joinedload(Order_inv.Order_inv_line)\
						.options(
							joinedload(Order_inv_line.resource)
						))

			if limit_by:
				order_invoices = order_invoices.limit(limit_by)
			order_invoices = order_invoices.all()

			for order_inv in order_invoices:
				invoice_models.append(order_inv)
		elif invoice_list:
			for invoice_index in invoice_list:
				OInvRegNo = invoice_index["OInvRegNo"]
				invoice_filtering["OInvRegNo"] = OInvRegNo
				order_inv = Order_inv.query\
					.filter_by(**invoice_filtering).first()
				if order_inv:
					invoice_models.append(order_inv)

	data = []
	fails = []
	for order_inv in invoice_models:
		try:
			order_inv_info = order_inv.to_json_api()

			inv_status = order_inv.inv_status.to_json_api() if order_inv.inv_status and not order_inv.inv_status.GCRecord else None
			inv_status = dataLangSelector(inv_status)
			order_inv_info["InvStatName"] = inv_status["InvStatName"]

			currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == order_inv.CurrencyId]

			if not currency_data:
				currency_data = [{"CurrencyCode": Config.DEFAULT_VIEW_CURRENCY_CODE}]
				# print("order_inv_api exception: no currency specified")
				# raise Exception

			this_Total = order_inv_info["OInvTotal"]
			this_FTotal = order_inv_info["OInvFTotal"]
			this_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None

			price_data = price_currency_conversion(
				priceValue = this_Total,
				from_currency = this_currencyCode,
				to_currency = currency_code,
				currencies_dbModel = currencies,
				exc_rates_dbModel = exc_rates)

			FTotal_price_data = price_currency_conversion(
				priceValue = this_FTotal,
				from_currency = this_currencyCode,
				to_currency = currency_code,
				currencies_dbModel = currencies,
				exc_rates_dbModel = exc_rates)

			order_inv_info["OInvTotal"] = price_data["ResPriceValue"]
			order_inv_info["OInvFTotal"] = FTotal_price_data["ResPriceValue"]
			order_inv_info["CurrencyId"] = price_data["CurrencyId"]
			order_inv_info["CurrencyCode"] = price_data["CurrencyCode"]
			order_inv_info["CurrencySymbol"] = price_data["CurrencySymbol"]


			rp_acc_data = {}
			if rp_acc_user:
				rp_acc_data = rp_acc_user.to_json_api()

			elif order_inv.rp_acc:
				rp_acc_data = order_inv.rp_acc.to_json_api()

			# !!! Deprecated
			rp_acc_data["Images"] = []

			order_inv_info["Rp_acc"] = rp_acc_data
			order_inv_info["UGuid"] = order_inv.user.UGuid if order_inv.user and not order_inv.user.GCRecord else None
			order_inv_info["CGuid"] = order_inv.company.CGuid if order_inv.company and not order_inv.company.GCRecord else None
			order_inv_info["WhGuid"] = order_inv.warehouse.WhGuid if order_inv.warehouse and not order_inv.warehouse.GCRecord else None
			order_inv_info["DivGuid"] = order_inv.division.DivGuid if order_inv.division and not order_inv.division.GCRecord else None
			order_inv_info["RpAccGuid"] = order_inv.rp_acc.RpAccGuid if order_inv.rp_acc and not order_inv.rp_acc.GCRecord else None
			order_inv_info["RpAccRegNo"] = order_inv.rp_acc.RpAccRegNo if order_inv.rp_acc and not order_inv.rp_acc.GCRecord else None
			order_inv_info["StatusUI"] = getInvStatusUi(order_inv.InvStatId)

			# !!! Check the send and get type of these params (root or structured?)
			rp_acc_user = None

			if invoices_only == False:
				order_inv_lines = []
				for order_inv_line in order_inv.Order_inv_line:
					if not order_inv_line.GCRecord:
						this_order_inv_line = order_inv_line.to_json_api()
						this_order_inv_line["ResRegNo"] = order_inv_line.resource.ResRegNo if order_inv_line.resource and not order_inv_line.resource.GCRecord else None
						this_order_inv_line["ResGuid"] = order_inv_line.resource.ResGuid if order_inv_line.resource and not order_inv_line.resource.GCRecord else None

						currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == order_inv_line.CurrencyId]

						if not currency_data:
							currency_data = [{"CurrencyCode": Config.DEFAULT_VIEW_CURRENCY_CODE}]
							# print("order_inv_api line exception: no currency specified")
							# raise Exception

						this_line_Price = this_order_inv_line["OInvLinePrice"]
						this_line_Total = this_order_inv_line["OInvLineTotal"]
						this_line_FTotal = this_order_inv_line["OInvLineFTotal"]
						this_line_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None
						ExcRateValue = this_order_inv_line["ExcRateValue"]

						price_data = price_currency_conversion(
							priceValue = this_line_Price,
							from_currency = this_line_currencyCode,
							to_currency = currency_code,
							currencies_dbModel = currencies,
							exc_rates_dbModel = exc_rates)

						Total_price_data = price_currency_conversion(
							priceValue = this_line_Total,
							from_currency = this_line_currencyCode,
							to_currency = currency_code,
							currencies_dbModel = currencies,
							exc_rates_dbModel = exc_rates)

						FTotal_price_data = price_currency_conversion(
							priceValue = this_line_FTotal,
							from_currency = this_line_currencyCode,
							to_currency = currency_code,
							currencies_dbModel = currencies,
							exc_rates_dbModel = exc_rates)

						this_order_inv_line["OInvLinePrice"] = price_data["ResPriceValue"]
						this_order_inv_line["CurrencyId"] = price_data["CurrencyId"]
						this_order_inv_line["CurrencyCode"] = price_data["CurrencyCode"]
						this_order_inv_line["CurrencySymbol"] = price_data["CurrencySymbol"]
						this_order_inv_line["OInvLineTotal"] = Total_price_data["ResPriceValue"]
						this_order_inv_line["OInvLineFTotal"] = FTotal_price_data["ResPriceValue"]


						if show_inv_line_resource:
							resource_json = apiResourceInfo(
								resource_list = [{"ResId": order_inv_line.ResId}],
								avoidQtyCheckup = 1,
								single_object = True)
							this_order_inv_line["Resource"] = resource_json["data"]

						order_inv_lines.append(this_order_inv_line)

				order_inv_info["Order_inv_lines"] = order_inv_lines
			data.append(order_inv_info)

		except Exception as ex:
			print(f"{datetime.now()} | Order_inv info utils Exception: {ex}")
			fails.append(order_inv.to_json_api())

	status = checkApiResponseStatus(data,fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		else:
			data = {}

		if len(fails) == 1:
			fails = fails[0]
		else:
			fails = {}

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


def apiInvInfo(
	startDate = None,
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
		invoice_filtering["InvStatId"] = statusId
	if rp_acc_user:
		invoice_filtering["RpAccId"] = rp_acc_user.RpAccId

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
			inv_info["InvStatName"] = inv_status["InvStatName"]

			if rp_acc_user:
				rpAccData = apiRpAccData(dbModel = rp_acc_user)
			else:
				# !!! TODO: optimize by adding joined query
				rp_acc_user = Rp_acc.query\
					.filter_by(GCRecord = None, RpAccId = invoice.RpAccId)\
					.first()
				rpAccData = apiRpAccData(dbModel = rp_acc_user)
			rp_acc_user = None
			inv_info["Rp_acc"] = rpAccData["data"]

			inv_lines = []
			for inv_line in invoice.Inv_line:
				if not inv_line.GCRecord:
					this_inv_line = inv_line.to_json_api()
					try:
						# !!! TODO: optimize by adding joined query
						resource = Resource.query\
							.filter_by(GCRecord = None, ResId = inv_line.ResId)\
							.first()
						resource_json = apiResourceInfo(resource_models=[resource],single_object=True)
						this_inv_line["Resource"] = resource_json["data"]

					except Exception as ex:
						print(f"{datetime.now()} | Invoice_line info utils Exception: {ex}")
						this_inv_line["Resource"] = []
					inv_lines.append(this_inv_line)

			inv_info["Inv_lines"] = inv_lines
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
