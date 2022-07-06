# -*- coding: utf-8 -*-
from flask import jsonify, request, abort, make_response

# datetime, date-parser
import dateutil.parser
import datetime as dt
from datetime import datetime
# / datetime, date-parser /

from main_pack import db
from . import api

# orders and db methods
from main_pack.models import (
	Invoice,
	Inv_line,
)
from .utils import (
	addInvDict,
	addInvLineDict
)
from .commerce_utils import apiInvInfo
from main_pack.base.apiMethods import checkApiResponseStatus
# / orders and db methods /

# Rp_acc db Model and methods
from main_pack.models import Rp_acc
# / Rp_acc db Model and methods /

# auth and validation
from main_pack.api.auth.utils import token_required
from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json
# / auth and validation /


@api.route("/tbl-dk-invoices/",methods=['GET','POST'])
@admin_required
@request_is_json(request)
def api_invoices(user):
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		startDate = request.args.get("startDate",None,type=str)
		endDate = request.args.get("endDate",datetime.now())

		res = apiInvInfo(
			startDate = startDate,
			endDate = endDate,
			statusId = 1,
			DivId = DivId,
			notDivId = notDivId)

		status_code = 200
		response = make_response(jsonify(res), status_code)
		return response

	elif request.method == 'POST':
		req = request.get_json()

		data = []
		failed_data = [] 

		for data in req:
			invoice = addInvDict(data)
			try:
				InvRegNo = invoice['InvRegNo']
				thisInv = Invoice.query.filter_by(InvRegNo = InvRegNo).first()
				# getting correct rp_acc of a database

				try:
					RpAccRegNo = data['Rp_acc']['RpAccRegNo']
					RpAccName = data['Rp_acc']['RpAccName']
					rp_acc = Rp_acc.query\
						.filter_by(RpAccRegNo = RpAccRegNo, RpAccName = RpAccName)\
						.first()
					if rp_acc:
						invoice['RpAccId'] = rp_acc.RpAccId
	
				except Exception as ex:
					print(f"{datetime.now()} | Inv Api Exception: {ex}")
					print("Rp_acc not provided")
					abort(400)

				thisInvStatus = None

				if thisInv:
					old_invoice_status = thisInv.InvStatId
					thisInv.update(**invoice)
					db.session.commit()
					thisInvStatus = thisInv.InvStatId

				else:
					thisInv = Invoice(**invoice)
					db.session.add(thisInv)
					db.session.commit()

				inv_lines = []
				failed_inv_lines = []

				for inv_line_req in data['inv_lines']:
					inv_line = addInvLineDict(inv_line_req)
					inv_line['InvId'] = thisInv.InvId
					try:
						InvLineRegNo = inv_line['InvLineRegNo']
						thisInvLine = Inv_line.query\
							.filter_by(InvLineRegNo = InvLineRegNo)\
							.first()
						if thisInvLine:
							thisInvLine.update(**inv_line)
						else:
							newInvLine = Inv_line(**inv_line)
							db.session.add(newInvLine)
						inv_lines.append(inv_line)
					except Exception as ex:
						print(f"{datetime.now()} | Inv Api Exception: {ex}")
						failed_inv_lines.append(inv_line)
					
				db.session.commit()
				invoice['inv_lines'] = inv_lines
				data.append(invoice)

			except Exception as ex:
				print(f"{datetime.now()} | Inv Api Exception: {ex}")
				failed_data.append(invoice)

		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data),
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response


@api.route("/tbl-dk-invoices/<InvRegNo>/")
@admin_required
def api_invoice_info(user, InvRegNo):
	invoice_list = [{"InvRegNo": InvRegNo}]
	res = apiInvInfo(
		invoice_list = invoice_list,
		single_object = True)

	status_code = 200 if res['status'] == 1 else 404
	response = make_response(jsonify(res), status_code)
	return response


# example request:
# api/v-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
@api.route("/v-invoices/",methods=['GET'])
@token_required
def api_v_invoices(user):
	startDate = request.args.get("startDate",None,type=str)
	endDate = request.args.get("endDate",datetime.now())
	current_user = user['current_user']
	res = apiInvInfo(
		startDate = startDate,
		endDate = endDate,
		rp_acc_user = current_user)

	status_code = 200
	response = make_response(jsonify(res), status_code)
	return response


@api.route("/v-invoices/<InvRegNo>/",methods=['GET'])
@token_required
def api_v_invoice(user,InvRegNo):
	current_user = user['current_user']
	invoice_list = [{"InvRegNo": InvRegNo}]
	res = apiInvInfo(
		invoice_list = invoice_list,
		single_object = True,
		rp_acc_user = current_user)

	status_code = 200 if res['status'] == 1 else 404
	response = make_response(jsonify(res), status_code)
	return response