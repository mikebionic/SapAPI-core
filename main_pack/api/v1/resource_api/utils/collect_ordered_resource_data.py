from main_pack.models import (
	Order_inv,
	Order_inv_line,
	Resource,
)
from sqlalchemy.orm import joinedload

from main_pack.base import log_print
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def collect_ordered_resource_data(ResId=None, ResGuid=None, limit=10):
	data, message = [], "With this product people also buy"
	try:
		if not ResId and not ResGuid:
			message = "No id or guid specified."
			raise Exception(message)

		res_filtering = {}
		if ResId:
			res_filtering["ResId"] = ResId
		if ResGuid:
			res_filtering["ResGuid"] = ResGuid
		thisResource = Resource.query.with_entities(Resource.ResId, Resource.ResGuid).filter_by(**res_filtering).first()
		if not thisResource:
			message = "Resource not found"
			raise Exception(message)

		all_inv_lines = Order_inv_line.query.with_entities(Order_inv_line.ResId, Order_inv_line.OInvId).filter_by(ResId = thisResource.ResId).all()
		if not all_inv_lines:
			message = "Data not available yet"
			raise Exception(message)

		order_ids_list = list(dict.fromkeys([oinv_line.OInvId for oinv_line in all_inv_lines if oinv_line.OInvId]))
		# try to get massive orders with more than 2 lines
		all_orders = Order_inv.query.filter(Order_inv.OInvId.in_(order_ids_list))\
			.options(joinedload(Order_inv.Order_inv_line))\
			.order_by(Order_inv.CreatedDate.desc())\
			.limit(100)\
			.all()
			# check this again
		if not all_orders:
			message = "Data not available yet"
			raise Exception(message)

		res_ids = []
		for this_order in all_orders:
			[res_ids.append(oinv_line.ResId) for oinv_line in this_order.Order_inv_line if oinv_line.ResId]
		counted_res_dict = dict((i, res_ids.count(i)) for i in res_ids)
		if ResId in counted_res_dict:
			del counted_res_dict[ResId]
		filtered_res_list_sorted = list({k: v for k, v in sorted(counted_res_dict.items(), key=lambda item: item[1])})[::-1][:limit]
		resource_list = [{"ResId": item} for item in filtered_res_list_sorted]

		data = apiResourceInfo(resource_list = resource_list)["data"]

	except Exception as ex:
		log_print(ex)

	return data, message