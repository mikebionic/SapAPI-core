from main_pack.models import Warehouse

def get_warehouse_id_guid_list():
	warehouses = Warehouse.query\
		.with_entities(Warehouse.WhId,Warehouse.WhGuid)\
		.filter_by(GCRecord = None)\
		.filter(Warehouse.WhGuid != None).all()

	warehouse_WhId_list = [warehouse.WhId for warehouse in warehouses]
	warehouse_WhGuid_list = [str(warehouse.WhGuid) for warehouse in warehouses]
	return warehouse_WhId_list, warehouse_WhGuid_list