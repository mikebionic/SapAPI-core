from main_pack.models import (
	Order_inv,
	Order_inv_line,
	Resource,
)

from main_pack.base import log_print
from main_pack.api.commerce.commerce_utils import apiResourceInfo

def collect_ordered_resource_data(ResId=None, ResGuid=None, limit=None):
	data, message = {}, ""
	try:
		if not ResId and not ResGuid:
			message = "No id or guid specified."
			raise Exception(message)

		filtering = {"GCRecord": None}
		if ResId:
			filtering["ResId"] = ResId
		if ResGuid:
			filtering["ResGuid"] = ResGuid
		thisResource = Resource.query.filter_by(**res_filtering).first()
		if not thisResource:
			message = "Resource not found"
			raise Exception(message)

		all_inv_lines = Order_inv_line.query.filter_by(ResId = thisResource.ResId).all()
		if not all_inv_lines:
			message = "Data not available yet"
			raise Exception(message)

		order_ids_list = list(dict.fromkeys([oinv_line.OInvId for oinv_line in all_inv_lines]))
		# try to get massive orders with more than 2 lines
		all_orders = Order_inv.query.filter(Order_inv.OInvId.in_(order_ids_list))\
			.options(joinedload(Order_inv.Order_inv_line))\
			.all()
			# check this again
		if not all_orders:
			message = "Data not available yet"
			raise Exception(message)
		# .limit(limit)

		# resource_list = [{"ResId": item} for item in list(dict.fromkeys([oinv_line.ResId for oinv_line in this_order.OInvLines for this_order in all_orders]))]
		filtered_res_list = list(dict.fromkeys([oinv_line.ResId for oinv_line in this_order.OInvLines for this_order in all_orders]))
		resource_list = [{"ResId": item} for item in filtered_res_list]

		# Check and get the most counted:
		# a = ["a", "b", "a"]
		# result = dict((i, a.count(i)) for i in a)
		# print result

		data = apiResourceInfo(resource_list = resource_list)["data"]

	except Exception as ex:
		log_print(ex)

	return data, message