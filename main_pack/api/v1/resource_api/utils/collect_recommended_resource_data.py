
from main_pack.api.commerce.commerce_utils import apiResourceInfo
from main_pack.base import log_print
from main_pack.models import (
	Order_inv,
	Order_inv_line,
	Rating,
	Wish,
	Resource,
	Res_category,
	Brand,
)

def collect_recommended_resource_data(rp_acc_user, limit=15):
	data, message = [], "Recommended resources"
	try:
		resource_ids = []
		rp_orders = Order_inv.query\
			.with_entities(Order_inv.OInvId, Order_inv.RpAccId)\
			.filter_by(RpAccId = rp_acc_user.RpAccId).all()
		if rp_orders:
			these_order_lines = Order_inv_line.query\
				.with_entities(Order_inv_line.ResId, Order_inv_line.OInvId)\
				.filter(Order_inv_line.OInvId.in_([order_inv.OInvId for order_inv in rp_orders]))\
				.all()
			[resource_ids.append(order_line.ResId) for order_line in these_order_lines if order_line.ResId]
		
		counted_res_dict = dict((i, resource_ids.count(i)) for i in resource_ids)
		resource_ids = list({k: v for k, v in sorted(counted_res_dict.items(), key=lambda item: item[1])})[::-1][:limit]
		
		rp_ratings = Rating.query\
			.with_entities(Rating.ResId, Rating.RpAccId, Rating.RtRatingValue)\
			.filter_by(RpAccId = rp_acc_user.RpAccId)\
			.filter(Rating.RtRatingValue >= 4).all()
		if rp_ratings:
			[resource_ids.append(rating.ResId) for rating in rp_ratings if rating.ResId]

		rp_wishlist = Wish.query\
			.with_entities(Wish.ResId, Wish.RpAccId, Wish.GCRecord)\
			.filter_by(RpAccId = rp_acc_user.RpAccId, GCRecord = None).all()
		if rp_wishlist:
			[resource_ids.append(wish.ResId) for wish in rp_wishlist]
		
		counted_res_dict = dict((i, resource_ids.count(i)) for i in resource_ids)
		resource_ids = list({k: v for k, v in sorted(counted_res_dict.items(), key=lambda item: item[1])})[::-1][:limit]
		if not resource_ids:
			message = "Data not available yet"
			raise Exception(message)
		
		all_res_models = Resource.query\
			.with_entities(Resource.BrandId, Resource.ResCatId, Resource.ResId)\
			.filter(Resource.ResId.in_(resource_ids))\
			.all()
		
		brand_ids = [this_resource.BrandId for this_resource in all_res_models if this_resource.BrandId]
		category_ids = [this_resource.ResCatId for this_resource in all_res_models if this_resource.ResCatId]
		brand_ids = list({k: v for k, v in sorted(dict((i, brand_ids.count(i)) for i in brand_ids).items(), key=lambda item: item[1])})[::-1][:limit]
		category_ids = list({k: v for k, v in sorted(dict((i, category_ids.count(i)) for i in category_ids).items(), key=lambda item: item[1])})[::-1][:limit]

		other_res_ids = []
		if brand_ids:
			all_brands = Brand.query\
				.with_entities(Brand.BrandId, Brand.BrandVisibleIndex, Brand.IsMain)\
				.filter(Brand.BrandId.in_(brand_ids))\
				.order_by(
					Brand.BrandVisibleIndex > 0,
					Brand.BrandVisibleIndex.desc(),
					Brand.IsMain.desc())\
				.limit(50)\
				.all()

			if all_brands:
				brand_resources = Resource.query\
					.with_entities(Resource.ResId, Resource.BrandId)\
					.filter(Resource.BrandId.in_([brand.BrandId for brand in all_brands]))\
					.order_by(
						Resource.ResVisibleIndex > 0, 
						Resource.ResVisibleIndex.desc(),
						Resource.ResViewCnt.desc())\
					.limit(50)\
					.all()
				[other_res_ids.append(this_resource.ResId) for this_resource in brand_resources if brand_resources]

		if category_ids:
			all_categories = Res_category.query\
				.with_entities(Res_category.ResCatId, Res_category.ResCatVisibleIndex, Res_category.IsMain)\
				.filter(Res_category.ResCatId.in_(category_ids))\
				.order_by(
					Res_category.ResCatVisibleIndex > 0, 
					Res_category.ResCatVisibleIndex.desc(), 
					Res_category.IsMain.desc())\
				.limit(50)\
				.all()

			if all_categories:
				category_resources = Resource.query\
					.with_entities(Resource.ResId, Resource.ResCatId)\
					.filter(Resource.ResCatId.in_([category.ResCatId for category in all_categories]))\
					.order_by(
						Resource.ResVisibleIndex > 0, 
						Resource.ResVisibleIndex.desc(),
						Resource.ResViewCnt.desc())\
					.limit(50)\
					.all()
				[other_res_ids.append(this_resource.ResId) for this_resource in category_resources if category_resources]

		counted_other_res_ids = dict((i, other_res_ids.count(i)) for i in other_res_ids)
		for ResId in resource_ids:
			if ResId in counted_other_res_ids:
				del counted_res_dict[ResId]

		other_res_ids = list({k: v for k, v in sorted(counted_other_res_ids.items(), key=lambda item: item[1])})[::-1][:limit]
		data = apiResourceInfo(resource_list = [{"ResId": item} for item in other_res_ids])["data"]

	except Exception as ex:
		log_print(ex)

	return data, message

#IsMain
#ResVisibleIndex
#ResViewCnt
#BrandId
#ResCatId

#category
#ResCatVisibleIndex
#IsMain

#brands
#BrandVisibleIndex
#IsMain

#Wishlist
#Rating 
#Order_inv