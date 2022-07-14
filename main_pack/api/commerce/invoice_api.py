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
	Resource,
	Res_total,
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

# import models division, warehouse, currency
from main_pack.models import Warehouse, Division, Currency

# auth and validation
from main_pack.api.auth.utils import sha_required, token_required
from main_pack.api.auth.utils import admin_required
from main_pack.api.base.validators import request_is_json
# / auth and validation /

from main_pack.base import log_print

@api.route("/tbl-dk-invoices/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_invoices():
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
		# print(req)

		divisions = Division.query\
			.filter_by(GCRecord = None)\
			.filter(Division.DivGuid != None).all()
		warehouses = Warehouse.query\
			.filter_by(GCRecord = None)\
			.filter(Warehouse.WhGuid != None).all()
		rp_accs = Rp_acc.query\
			.filter_by(GCRecord = None)\
			.filter(Rp_acc.RpAccGuid != None).all()
		

		division_DivId_list = [division.DivId for division in divisions]
		division_DivGuid_list = [str(division.DivGuid) for division in divisions]

		warehouse_WhId_list = [warehouse.WhId for warehouse in warehouses]
		warehouse_WhGuid_list = [str(warehouse.WhGuid) for warehouse in warehouses]

		rp_acc_RpAccId_list = [rp_acc.RpAccId for rp_acc in rp_accs]
		rp_acc_RpAccGuid_list = [str(rp_acc.RpAccGuid) for rp_acc in rp_accs]

		currencies = Currency.query.filter_by(GCRecord = None).all()

		data = []
		failed_data = [] 

		for inv_req in req:
			try:
				invoice = addInvDict(inv_req)
				DivGuid = inv_req['DivGuid']
				WhGuid = inv_req['WhGuid']
				RpAccGuid = inv_req['RpAccGuid']

				InvGuid = invoice['InvGuid']
				InvRegNo = invoice['InvRegNo']

				try:
					indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
					DivId = int(indexed_div_id)
				except:
					DivId = None
				try:
					indexed_wh_id = warehouse_WhId_list[warehouse_WhGuid_list.index(WhGuid)]
					WhId = int(indexed_wh_id)
				except:
					WhId = None
				try:
					indexed_rp_acc_id = rp_acc_RpAccId_list[rp_acc_RpAccGuid_list.index(RpAccGuid)]
					RpAccId = int(indexed_rp_acc_id)
				except:
					RpAccId = None

				invoice['DivId'] = DivId
				invoice['WhId'] = WhId
				invoice['RpAccId'] = RpAccId



				thisInv = Invoice.query\
					.filter_by(
						InvRegNo = InvRegNo,
						GCRecord = None)\
					.first()
				
				if not RpAccId or not DivId or not WhId:
					log_print(f"RpAccId - {RpAccId} by {RpAccGuid} | DivId - {DivId} by {DivGuid}, WhId - {WhId} | by {WhGuid}")
					raise Exception

				thisInvStatus = None

				if thisInv:
					if thisInv.InvGuid == InvGuid:
						old_invoice_status = thisInv.InvStatId
						thisInv.update(**invoice)
						db.session.commit()
						thisInvStatus = thisInv.InvStatId
					else:
						log_print("InvGuid or RegNo has changed ", InvGuid, InvRegNo, thisInv.to_json_api())
						raise Exception


				else:
					thisInv = Invoice(**invoice)
					db.session.add(thisInv)
					db.session.commit()
					# db.session.commit()

				
				inv_lines = []
				
				failed_inv_lines = []


				for inv_line_req in inv_req['Inv_lines']:
					inv_line = addInvLineDict(inv_line_req)
					inv_line['InvId'] = thisInv.InvId
					ResRegNo = inv_line_req['ResRegNo']
					ResGuid = inv_line_req['ResGuid']

					this_line_resource = Resource.query\
						.filter_by(
							ResRegNo = ResRegNo,
							ResGuid = ResGuid,
							GCRecord = None)\
						.first()
					try:
						inv_line["ResId"] = this_line_resource.ResId
						InvLineGuid = inv_line['InvLineGuid']
						InvLineRegNo = inv_line['InvLineRegNo']
						thisInvLine = Inv_line.query\
							.filter_by(InvLineRegNo = InvLineRegNo)\
							.first()


						if thisInvLine:
							thisInvLine.update(**inv_line)
							if thisInvStatus == 9 or thisInvStatus == 5:
								try:
									if (old_invoice_status != 5 or old_invoice_status != 9):
										res_total = Res_total.query\
											.filter_by(
												ResId = thisInvLine.ResId,
												GCRecord = None)\
											.first()
										res_total.ResPendingTotalAmount += thisInvLine.InvLineAmount

								except Exception as ex:
									log_print(f"Inv Api Res_total Exception: {ex}")
							db.session.commit()
							inv_lines.append(inv_line_req)
								

						else:
							
							newInvLine = Inv_line(**inv_line)
							db.session.add(newInvLine)
							db.session.commit()
							inv_lines.append(inv_line)
							thisInvLine = None
					except Exception as ex:
						print(f"{datetime.now()} | Inv Api Exception: {ex}")
						failed_inv_lines.append(inv_line)
					
				db.session.commit()
				invoice['Inv_lines'] = inv_lines
				data.append(invoice)

			except Exception as ex:
				print(f"{datetime.now()} | Inv Api exception: {ex}")
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