
# data = {
# 	'data': {
# 		'OInvId': 57,
# 		'OInvGuid': '031f0dfb-bede-4148-a619-bc7b28ca575c',
# 		'OInvTypeId': 2,
# 		'InvStatId': 1,
# 		'CurrencyId': 1,
# 		'RpAccId': 44,
# 		'CId': 1,
# 		'UId': 1,
# 		'DivId': 1,
# 		'WhId': 1,
# 		'WpId': 1,
# 		'EmpId': None,
# 		'PtId': 1,
# 		'PmId': 1,
# 		'PaymStatusId': None,
# 		'PaymCode': None,
# 		'PaymDesc': None,
# 		'OInvLatitude': 0.0,
# 		'OInvLongitude': 0.0,
# 		'OInvRegNo': 'MASSFK711224575',
# 		'OInvDesc': 'dushundirish uyazu\n',
# 		'OInvDate': '2021-06-17 14:22:06',
# 		'OInvTotal': 230.0,
# 		'OInvExpenseAmount': 0.0,
# 		'OInvTaxAmount': 0.0,
# 		'OInvDiscountAmount': 0.0,
# 		'OInvPaymAmount': 0.0,
# 		'OInvFTotal': 230.0,
# 		'OInvFTotalInWrite': 'iki ýüz otuz manat nol teňňe',
# 		'OInvModifyCount': 0,
# 		'OInvPrintCount': 0,
# 		'OInvCreditDays': 0,
# 		'OInvCreditDesc': None,
# 		'AddInf1': None,
# 		'AddInf2': None,
# 		'AddInf3': None,
# 		'AddInf4': None,
# 		'AddInf5': "{'date': '2021-06-17 14:22:06',	'info': 'Browser: chrome, Platform: linux, Details: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}",
# 		'AddInf6': None,
# 		'CreatedDate': '2021-06-17 14:01:51',
# 		'ModifiedDate': '2021-06-17 14:01:51',
# 		'SyncDateTime': '2021-06-17 14:01:51',
# 		'CreatedUId': None,
# 		'ModifiedUId': None,
# 		'GCRecord': None
# 	},
# 	'successes': [
# 		{
# 			'OInvLineId': None,
# 			'OInvLineGuid': '1315e8ad-400d-43ec-a74f-581e7479c96d',
# 			'OInvId': 57,
# 			'UnitId': 1,
# 			'CurrencyId': 1,
# 			'ResId': '7',
# 			'LastVendorId': None,
# 			'OInvLineRegNo': ('MASSK901682527', None),
# 			'OInvLineDesc': None,
# 			'OInvLineAmount': 2.0,
# 			'OInvLinePrice': 115.0,
# 			'OInvLineTotal': 230.0,
# 			'OInvLineExpenseAmount': 0,
# 			'OInvLineTaxAmount': 0,
# 			'OInvLineDiscAmount': 0,
# 			'OInvLineFTotal': 230.0,
# 			'OInvLineDate': None,
# 			'ExcRateValue': 30.0,
# 			'AddInf1': None,
# 			'AddInf2': None,
# 			'AddInf3': None,
# 			'AddInf4': None,
# 			'AddInf5': None,
# 			'AddInf6': None,
# 			'CreatedDate': None,
# 			'ModifiedDate': None,
# 			'SyncDateTime': None,
# 			'CreatedUId': None,
# 			'ModifiedUId': None,
# 			'GCRecord': None
# 		}
# 	],
# 	'fails': [],
# 	'success_total': 1,
# 	'fail_total': 0,
# 	'total': 1,
# 	'status': 1,
# 	'message': 'Success'
# }

from main_pack.models import (
	Warehouse,
	Work_period,
	Resource,
	Rp_acc,
	User,
	Division,
)

def send_order_to_server(data, dbModel = None):
	try:
		if dbModel:
			payload = dbModel.to_json_api()
			payload["UGuid"] = dbModel.user.UGuid
			payload["RpAccGuid"] = dbModel.rp_acc.RpAccGuid
			payload["DivGuid"] = dbModel.division.DivGuid
			payload["WhGuid"] = dbModel.warehouse.WhGuid
			# payload["WpGuid"] = dbModel.work_period.WpGuid

			inv_lines_payload = []
			for inv_line in dbModel.Order_inv_line:
				current_inv_line = inv_line.to_json_api()
				current_inv_line["ResGuid"] = inv_line.resource.ResGuid
				inv_lines_payload.append(current_inv_line)

			payload["Order_inv_lines"] = inv_lines_payload

		else:
			if data["status"] != 1:
				raise Exception

			payload = data["data"]

			this_warehouse = Warehouse.query.get(payload["WhId"])
			if this_warehouse:
				payload["WhGuid"] = this_warehouse.WhGuid

			this_rp_acc = Rp_acc.query.get(payload["RpAccId"])
			if this_rp_acc:
				payload["RpAccGuid"] = this_rp_acc.RpAccGuid

			this_user = User.query.get(payload["UId"])
			if this_user:
				payload["UGuid"] = this_user.UGuid

			this_division = Division.query.get(payload["DivId"])
			if this_division:
				payload["DivGuid"] = this_division.DivGuid

			# this_work_period = Work_period.query.get(payload["WpId"])
			# if this_work_period:
			# 	payload["WpGuid"] = this_work_period.WpGuid

			inv_lines_payload = []
			for inv_line in data["successes"]:
				current_inv_line = inv_line.copy()

				this_resource = Resource.query.get(inv_line["ResId"])
				if this_resource:
					current_inv_line["ResGuid"] = this_resource.ResGuid
					inv_lines_payload.append(current_inv_line)

			payload["Order_inv_lines"] = inv_lines_payload


		# send request
	except Exception as ex:
		print(ex)