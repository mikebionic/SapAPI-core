
# orders and db methods
from sqlalchemy import extract, and_
from main_pack.base.apiMethods import checkApiResponseStatus
from sqlalchemy import and_, extract
# / orders and db methods /

# orders and db methods
from main_pack.models.commerce.models import (Order_inv,
																							Order_inv_line,
																							Inv_status)
from main_pack.api.commerce.utils import (addOrderInvDict,
																					addOrderInvLineDict)
from main_pack.base.apiMethods import checkApiResponseStatus
from sqlalchemy import and_, extract
# / orders and db methods /

# Rp_acc methods
from main_pack.api.users.utils import apiRpAccData
# / Rp_acc methods /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /

# example request
@api.route("/tbl-dk-order-invoices/filter/")
@sha_required
def api_order_invoices_filter():	
	startDate = request.args.get('startDate',None,type=str)
	endDate = request.args.get('endDate',datetime.now().date())

	order_invoices = apiOrderInvInfo(startDate,endDate,statusId=1)

	res = {
		"status": 1,
		"message": "All order invoices between dates",
		"data": order_invoices,
		"total": len(order_invoices)
	}
	response = make_response(jsonify(res),200)
	return response

@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	order_invoices = apiOrderInvInfo(startDate,endDate,user=current_user)

	res = {
		"status": 1,
		"message": "Orders",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res),200)
	return response

@api.route("/v-order-invoices/<OInvRegNo>/",methods=['GET'])
@token_required
def api_v_order_invoice(user,OInvRegNo):
	model_type = user['model_type']
	current_user = user['current_user']
	
	invoice_list = [{"OInvRegNo": OInvRegNo}]
	order_invoices = apiOrderInvInfo(invoice_list,
																	single_object=True,
																	user=current_user)
#########################


def apiOrderInvInfo(startDate=None,
										endDate=datetime.now(),
										statusId=None,
										single_object=False,
										invoice_list=None,
										rp_acc_user=None):
	inv_statuses = Inv_status.query\
		.filter_by(GCRecord = None).all()

	order_filtering = {
		"GCRecord": None
	}
	if statusId:
		order_filtering['InvStatId'] = statusId
	if rp_acc_user:
		order_filtering['RpAccId'] = rp_acc_user.RpAccId

	order_inv_models = []
	if invoice_list is None:
		if startDate == None:
			order_invoices = Order_inv.query\
				.filter_by(**order_filtering)\
				.order_by(Order_inv.OInvDate.desc()).all()
		else:
			# filtering by date
			if (type(startDate)!=datetime):
				startDate = dateutil.parser.parse(startDate)
				startDate = datetime.date(startDate)
				print(startDate)
			if (type(endDate)!=datetime):
				print(type(endDate))
				endDate = dateutil.parser.parse(endDate)
				endDate = datetime.date(endDate)
				print(endDate)
			order_invoices = Order_inv.query\
			.filter_by(**order_filtering)\
			.filter(and_(
				extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
				extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
				extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))\
			.order_by(Order_inv.OInvDate.desc()).all()
		for order_inv in order_invoices:
			order_inv_models.append(order_inv)
	else:
		for invoice_index in invoice_list:
			OInvRegNo = invoice_index["OInvRegNo"]
			order_filtering["OInvRegNo"] = OInvRegNo
			order_inv = Order_inv.query\
				.filter_by(**order_filtering).first()
			if order_inv:
				order_inv_models.append(order_inv)

	data = []
	fails = []
	for order_inv in order_inv_models:
		try:
			order_inv_info = order_inv.to_json_api()

			inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_inv.InvStatId]
			inv_status = dataLangSelector(inv_status_list[0])
			order_inv_info['InvStatName'] = inv_status['InvStatName']

			if rp_acc_user:
				rpAccData = apiRpAccData(dbModel=rp_acc_user)
			else:
				rp_acc = Rp_acc.query.filter_by(
						GCRecord = None, RpAccId = order_inv.RpAccId).first()
				rpAccData = apiRpAccData(dbModel=rp_acc)
			order_inv_info['Rp_acc'] = rpAccData['data']

			order_inv_info['Order_inv_lines'] = [order_inv_line.to_json_api() for order_inv_line in order_inv.Order_inv_line if order_inv_line.GCRecord == None]
			data.append(order_inv_info)
		except Exception as ex:
			print(ex)
			fails.append(order_inv.to_json_api())
	status = checkApiResponseStatus(data,fails)
	if single_object == True:
		if len(data) == 1:
			data = data[0]
		if len(fails) == 1:
			fails = fails[0]
	res = {
			"message": "Order invoice",
			"data": data,
			"fails": fails,
			"total": len(data),
			"fail_total": len(fails)
	}
	for e in status:
		res[e] = status[e]
	return res