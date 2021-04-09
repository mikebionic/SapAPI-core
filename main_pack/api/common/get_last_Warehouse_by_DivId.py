from main_pack.models import Warehouse

def get_last_Warehouse_by_DivId(DivId):
	data = Warehouse.query\
		.filter_by(DivId = DivId, GCRecord = None)\
		.order_by(Warehouse.WhId.asc())\
		.first()
	return data