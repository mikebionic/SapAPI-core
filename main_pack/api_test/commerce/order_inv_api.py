from flask import render_template,url_for,jsonify,request,abort,make_response,redirect
from main_pack.api_test.commerce import api
from main_pack import db_test
from flask import current_app

# orders and db methods
from main_pack.models_test.commerce.models import (Order_inv,
																							Order_inv_line,
																							Inv_status)
from main_pack.api_test.commerce.utils import (addOrderInvDict,
																					addOrderInvLineDict)
from main_pack.base.apiMethods import checkApiResponseStatus
from sqlalchemy import and_, extract
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models_test.users.models import Rp_acc
from main_pack.api_test.users.utils import apiRpAccData
# / Rp_acc db Model and methods /

# functions and methods
from main_pack.base.languageMethods import dataLangSelector
# / functions and methods /

# auth and validation
from main_pack.api_test.auth.api_login import token_required
from main_pack.api_test.auth.api_login import sha_required
# / auth and validation /

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /

@api.route("/tbl-dk-order-invoices/",methods=['GET','POST'])
@sha_required
def api_order_invoices():
	if request.method == 'GET':
		data=[]
		order_invoices = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.InvStatId==1)).all()
		inv_statuses = Inv_status.query.all()
		for order_invoice in order_invoices:
			oInvData = order_invoice.to_json_api()
			# !!! put order inv and inv fetch as a separate function
			inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_invoice.InvStatId]
			inv_status = dataLangSelector(inv_status_list[0])
			oInvData['InvStatName'] = inv_status['InvStatName']
		
			rp_acc = Rp_acc.query\
				.filter(and_(
					Rp_acc.GCRecord == '' or Rp_acc.GCRecord == None),\
					Rp_acc.RpAccId == order_invoice.RpAccId)\
				.first()
			if rp_acc:
				rpAccData = apiRpAccData(dbModel=rp_acc)
				oInvData['Rp_acc'] = rpAccData['data']

			order_inv_lines = Order_inv_line.query\
				.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
					Order_inv_line.OInvId==order_invoice.OInvId).all()

			order_inv_lines_list = []
			for order_inv_line in order_inv_lines:
				order_inv_lines_list.append(order_inv_line.to_json_api())
			oInvData['Order_inv_lines'] = order_inv_lines_list

			data.append(oInvData)
		res = {
			"status": 1,
			"message": "All order invoices",
			"data": data,
			"total": len(order_invoices)
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
			order_invoices = []
			failed_order_invoices = [] 
			for data in req:
				order_invoice = addOrderInvDict(data)
				print(order_invoice)
				try:
					OInvRegNo = order_invoice['OInvRegNo']
					thisOrderInv = Order_inv.query\
						.filter(Order_inv.OInvRegNo == OInvRegNo).first()
					# getting correct rp_acc of a database
					try:
						RpAccRegNo = data['Rp_acc']['RpAccRegNo']
						RpAccName = data['Rp_acc']['RpAccName']
						rp_acc = Rp_acc.query\
							.filter(Rp_acc.RpAccRegNo == RpAccRegNo and Rp_acc.RpAccName == RpAccName)\
							.first()
						if rp_acc:
							order_invoice['RpAccId'] = rp_acc.RpAccId
					except Exception as ex:
						print(ex)
						print("Rp_acc not provided")
						abort(400)

					if thisOrderInv:
						thisOrderInv.update(**order_invoice)
						db_test.session.commit()
					else:
						thisOrderInv = Order_inv(**order_invoice)
						db_test.session.add(thisOrderInv)
						db_test.session.commit()

					order_inv_lines = []
					failed_order_inv_lines = []
					for order_inv_line in data['Order_inv_lines']:
						order_inv_line = addOrderInvLineDict(order_inv_line)
						order_inv_line['OInvId'] = thisOrderInv.OInvId
						try:
							OInvLineRegNo = order_invoice['OInvLineRegNo']
							thisOrderInvLine = Order_inv_line.query\
								.filter(Order_inv_line.OInvLineRegNo == OInvLineRegNo).first()
							if thisOrderInvLine:
								thisOrderInvLine.update(**order_inv_line)
								db_test.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line updated')
							else:
								newOrderInvLine = Order_inv_line(**order_inv_line)
								db_test.session.add(newOrderInvLine)
								db_test.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line created')
						except Exception as ex:
							failed_order_inv_lines.append(order_inv_line)

					order_invoice['Order_inv_lines'] = order_inv_lines
					order_invoices.append(order_invoice)

				except Exception as ex:
					failed_order_invoices.append(order_invoice)

			status = checkApiResponseStatus(order_invoices,failed_order_invoices)
			res = {
				"data": order_invoices,
				"fails": failed_order_invoices,
				"success_total": len(order_invoices),
				"fail_total": len(failed_order_invoices),
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)

	return response


# example request:
# api/tbl-dk-order-invoices/filter/?statDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/tbl-dk-order-invoices/filter/")
@sha_required
def api_order_invoices_filter():
	# initialize statuses
	inv_statuses = Inv_status.query.all()
	
	startDate = request.args.get('startDate',None,type=str)
	endDate = request.args.get('endDate',datetime.now().date())
	if startDate == None:
		order_invoices = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.InvStatId==1))\
			.order_by(Order_inv.OInvDate.desc()).all()
	else:
		if (type(startDate)!=datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate)!=datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)
			
		order_invoices = Order_inv.query\
		.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
			Order_inv.InvStatId==1,\
			extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
			extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
			extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))\
		.order_by(Order_inv.OInvDate.desc()).all()

	data = []
	for order_invoice in order_invoices:
		oInvData = order_invoice.to_json_api()

		inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_invoice.InvStatId]
		inv_status = dataLangSelector(inv_status_list[0])
		oInvData['InvStatName'] = inv_status['InvStatName']
		
		rp_acc = Rp_acc.query\
				.filter(and_(
					Rp_acc.GCRecord == '' or Rp_acc.GCRecord == None),\
					Rp_acc.RpAccId == order_invoice.RpAccId)\
				.first()
		if rp_acc:
			rpAccData = apiRpAccData(dbModel=rp_acc)
			oInvData['Rp_acc'] = rpAccData['data']

		order_inv_lines = Order_inv_line.query\
			.filter(and_(
				Order_inv_line.GCRecord == '' or Order_inv_line.GCRecord == None),\
				Order_inv_line.OInvId == order_invoice.OInvId).all()

		order_inv_lines_list = []
		for order_inv_line in order_inv_lines:
			order_inv_lines_list.append(order_inv_line.to_json_api())
		oInvData['Order_inv_lines'] = order_inv_lines_list

		data.append(oInvData)
	res = {
		"status": 1,
		"message": "All order invoices between dates",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res),200)
	return response

# example request:
# api/v-order-invoices/?statDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-order-invoices/",methods=['GET'])
@token_required
def api_v_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	if model_type=='Rp_acc':
		RpAccId = current_user.RpAccId

	inv_statuses = Inv_status.query.all()
	
	startDate = request.args.get('startDate',None,type=str)
	endDate = request.args.get('endDate',datetime.now().date())
	if startDate == None:
		# !!! usage status is configurable, rp acc provided
		order_invoices = Order_inv.query\
			.filter(and_(
				Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.RpAccId==RpAccId))\
			.order_by(Order_inv.OInvDate.desc()).all()
	else:
		if (type(startDate)!=datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate)!=datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)
			
		order_invoices = Order_inv.query\
		.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
			Order_inv.RpAccId==RpAccId,\
			extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
			extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
			extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))\
		.order_by(Order_inv.OInvDate.desc()).all()

	data = []
	for order_invoice in order_invoices:
		oInvData = order_invoice.to_json_api()

		inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_invoice.InvStatId]
		inv_status = dataLangSelector(inv_status_list[0])
		oInvData['InvStatName'] = inv_status['InvStatName']
		
		order_inv_lines = Order_inv_line.query\
			.filter(and_(
				Order_inv_line.GCRecord == '' or Order_inv_line.GCRecord == None),\
				Order_inv_line.OInvId == order_invoice.OInvId).all()

		order_inv_lines_list = []
		for order_inv_line in order_inv_lines:
			order_inv_lines_list.append(order_inv_line.to_json_api())
		oInvData['Order_inv_lines'] = order_inv_lines_list

		data.append(oInvData)
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

	if model_type=='Rp_acc':
		RpAccId = current_user.RpAccId

		order_invoice = Order_inv.query\
			.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
				Order_inv.RpAccId==RpAccId,\
				Order_inv.OInvRegNo==OInvRegNo).first()

		order_inv_lines = Order_inv_line.query\
			.filter(and_(Order_inv_line.GCRecord=='' or Order_inv_line.GCRecord==None),\
				Order_inv_line.OInvId==order_invoice.OInvId).all()

		order_invoice = order_invoice.to_json_api()
		order_inv_lines_list = []
		for order_inv_line in order_inv_lines:
			order_inv_lines_list.append(order_inv_line.to_json_api())

		order_invoice['Order_inv_lines'] = order_inv_lines_list
		res = {
			"data": order_invoice,
			"total": len(order_inv_lines_list),
			"status": 1,
			"message": "Order lines"
		}
		response = make_response(jsonify(res),200)
	return response