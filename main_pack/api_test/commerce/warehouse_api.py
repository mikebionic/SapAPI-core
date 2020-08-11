from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api_test.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models_test.base.models import Warehouse
from main_pack.api_test.commerce.utils import addWarehouseDict
from main_pack import db_test
from flask import current_app
from main_pack.api_test.auth.api_login import sha_required

@api.route("/tbl-dk-warehouses/",methods=['GET','POST'])
@sha_required
def api_warehouses():
	if request.method == 'GET':
		warehouses = Warehouse.query.filter_by(GCRecord = None).all()
		res = {
			"status": 1,
			"message": "All warehouses",
			"data": [warehouse.to_json_api() for warehouse in warehouses],
			"total": len(warehouses)
		}
		response = make_response(jsonify(res),200)

	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)
			
		else:
			req = request.get_json()
			warehouses = []
			failed_warehouses = [] 
			for warehouse in req:
				warehouse = addWarehouseDict(warehouse)
				try:
					if not 'WhId' in warehouse:
						newWarehouse = Warehouse(**warehouse)
						db_test.session.add(newWarehouse)
						db_test.session.commit()
						warehouses.append(warehouse)
					else:
						WhId = warehouse['WhId']
						thisWarehouse = Warehouse.query.get(int(WhId))
						if thisWarehouse is not None:
							# check for presenting in database
							thisWarehouse.update(**warehouse)
							# thisWarehouse.modifiedInfo(UId=1)
							db_test.session.commit()
							warehouses.append(warehouse)

						else:
							# create new warehouse
							newWarehouse = Warehouse(**warehouse)
							db_test.session.add(newWarehouse)
							db_test.session.commit()
							warehouses.append(warehouse)
				except Exception as ex:
					print(ex)
					failed_warehouses.append(warehouse)

			status = checkApiResponseStatus(warehouses,failed_warehouses)
			res = {
				"data": warehouses,
				"fails": failed_warehouses,
				"success_total": len(warehouses),
				"fail_total": len(failed_warehouses)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)
			
	return response
