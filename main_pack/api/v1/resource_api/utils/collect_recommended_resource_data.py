
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

def collect_recommended_resource_data(rp_acc_user, limit=10):
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
		#print(resource_ids)
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

		if brand_ids:
			all_brands = Brand.query.filter(Brand.BrandId.in_(brand_ids))\
				.order_by(Brand.BrandVisibleIndex > 0)\
				.order_by(Brand.BrandVisibleIndex.desc())\
				.order_by(Brand.IsMain.desc())\
				.all()

		#if category_ids:
		#	all_categorys = category.query.filter(category.categoryId.in_(category_ids))\
		#		.order_by(category.categoryVisibleIndex > 0)\
		#		.order_by(category.categoryVisibleIndex.desc())\
		#		.order_by(category.IsMain.desc())\
		#		.all()

		#final = Resource.query\
		#	.filter(Resource.ResId.in_(resource_ids))\
		#	.filter(Resource.ResViewCnt > 0)\
		#	.order_by(Resource.ResViewCnt.desc())\
		#	.all()
			#.filter(Resource.IsMain > 0)\
			#.filter(Resource.ResVisibleIndex > 0)\
			#.order_by(Resource.ResVisibleIndex.asc())\


	except Exception as ex:
		log_print(ex)

	return data, message

#IsMain
#ResVisibleIndex
#ResViewCnt
#BrandId
#ResCatId
#Rating?

#category
#ResCatVisibleIndex
#IsMain

#brands
#BrandVisibleIndex
#IsMain

#Wishlist
#Rating 
#Order_inv