from main_pack.api.common import send_data_to_sync_server

from main_pack.models import (
	Warehouse,
	Resource,
	Rp_acc,
	User,
	Division,
)

def send_order_to_server(
	data,
	dbModel = None,
	host = None,
	port = None,
	url_path = None,
	token = None
):
	try:
		if dbModel:
			payload = dbModel.to_json_api()
			payload["OInvGuid"] = str(payload["OInvGuid"])
			payload["UGuid"] = str(dbModel.user.UGuid)
			payload["RpAccGuid"] = str(dbModel.rp_acc.RpAccGuid)
			payload["DivGuid"] = str(dbModel.division.DivGuid)
			payload["WhGuid"] = str(dbModel.warehouse.WhGuid)

			inv_lines_payload = []
			for inv_line in dbModel.Order_inv_line:
				current_inv_line = inv_line.to_json_api()
				current_inv_line["OInvLineGuid"] = str(current_inv_line["OInvLineGuid"])
				current_inv_line["ResGuid"] = str(inv_line.resource.ResGuid)
				inv_lines_payload.append(current_inv_line)

			payload["Order_inv_lines"] = inv_lines_payload

		else:
			if data["status"] != 1:
				raise Exception

			payload = data["data"]

			this_warehouse = Warehouse.query.get(payload["WhId"])
			if this_warehouse:
				payload["WhGuid"] = str(this_warehouse.WhGuid)

			this_rp_acc = Rp_acc.query.get(payload["RpAccId"])
			if this_rp_acc:
				payload["RpAccGuid"] = str(this_rp_acc.RpAccGuid)

			this_user = User.query.get(payload["UId"])
			if this_user:
				payload["UGuid"] = str(this_user.UGuid)

			this_division = Division.query.get(payload["DivId"])
			if this_division:
				payload["DivGuid"] = str(this_division.DivGuid)

			inv_lines_payload = []
			for inv_line in data["successes"]:
				current_inv_line = inv_line.copy()

				this_resource = Resource.query.get(inv_line["ResId"])
				if this_resource:
					current_inv_line["ResGuid"] = str(this_resource.ResGuid)
					inv_lines_payload.append(current_inv_line)

			payload["Order_inv_lines"] = inv_lines_payload

		send_data_to_sync_server(payload, host, port, url_path, token)

	except Exception as ex:
		print(ex)
