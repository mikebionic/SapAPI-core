
from main_pack.models import (
	Res_discount,
	Resource
)

from main_pack.api.commerce.commerce_utils import apiResourceInfo

def collect_discount_resource_data(limit=None):
	if limit:
		discount_resources = Res_discount.query.limit(limit).all()
	else:
		discount_resources = Res_discount.query.all()

	resource_list = []
	for disc in discount_resources:
		resource_list.append({"ResId": disc.SaleResId})
	
	data = apiResourceInfo(resource_list = resource_list)
	return data["data"]