# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack import db
from . import api
from .utils import addRpAccTrTotDict

from main_pack.models import Company, Division
from main_pack.models import Rp_acc, User
from main_pack.models import Rp_acc_trans_total

from main_pack.base.apiMethods import checkApiResponseStatus, fileToURL
from main_pack.api.auth.utils import sha_required, token_required
from main_pack.api.base.validators import request_is_json
from main_pack.api.users.utils import addRpAccDict


def get_rp_accs(
	DivId = None,
	DivGuid = None,
	notDivId = None,
	synchDateTime = None,
	RpAccId = None,
	RpAccRegNo = None,
	RpAccName = None,
	UId = None,
	EmpId = None,
	withPassword = 0):

	filtering = {"GCRecord": None}

	if RpAccId:
		filtering["RpAccId"] = RpAccId
	if RpAccRegNo:
		filtering["RpAccRegNo"] = RpAccRegNo
	if RpAccName:
		filtering["RpAccName"] = RpAccName
	if DivId:
		filtering["DivId"] = DivId
	if UId:
		filtering["UId"] = UId
	if EmpId:
		filtering["EmpId"] = EmpId

	rp_accs = Rp_acc.query.filter_by(**filtering)\
		.options(
			joinedload(Rp_acc.company),
			joinedload(Rp_acc.division),
			joinedload(Rp_acc.user),
			joinedload(Rp_acc.Rp_acc_trans_total),
			joinedload(Rp_acc.Image))

	if DivGuid:
		rp_accs = rp_accs\
			.join(Division, Division.DivId == Rp_acc.DivId)\
			.filter(Division.DivGuid == DivGuid)

	if notDivId:
		rp_accs = rp_accs.filter(Rp_acc.DivId != notDivId)

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		rp_accs = rp_accs.filter(Rp_acc.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

	rp_accs = rp_accs.all()

	data = []
	for rp_acc in rp_accs:
		rp_acc_info = rp_acc.to_json_api()
		rp_acc_info["DivGuid"] = rp_acc.division.DivGuid if rp_acc.division and not rp_acc.division.GCRecord else None
		rp_acc_info["CGuid"] = rp_acc.company.CGuid if rp_acc.company and not rp_acc.company.GCRecord else None
		rp_acc_info["UGuid"] = rp_acc.user.UGuid if rp_acc.user and not rp_acc.user.GCRecord else None
		rp_acc_info["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=rp_acc.Image[-1].FileName) if rp_acc.Image else ""
		rp_acc_info["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=rp_acc.Image[-1].FileName) if rp_acc.Image else ""
		rp_acc_info["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=rp_acc.Image[-1].FileName) if rp_acc.Image else ""

		if withPassword:
			rp_acc_info["RpAccUPass"] = rp_acc.RpAccUPass

		trans_total = [rp_acc_trans_total.to_json_api()
			for rp_acc_trans_total in rp_acc.Rp_acc_trans_total 
			if not rp_acc_trans_total.GCRecord]

		total_info = trans_total[0] if trans_total else {}
		rp_acc_info["RpAccTransTotal"] = total_info
		trans_total = None

		data.append(rp_acc_info)

	return data


@api.route("/v-rp-accs/")
@token_required
def api_v_rp_accs():
	arg_data = {
		"DivId": request.args.get("DivId",None,type=int),
		"DivGuid": request.args.get("DivGuid",None,type=str),
		"notDivId": request.args.get("notDivId",None,type=int),
		"synchDateTime": request.args.get("synchDateTime",None,type=str),
		"RpAccId": request.args.get("id",None,type=int),
		"RpAccRegNo": request.args.get("regNo","",type=str),
		"RpAccName": request.args.get("name","",type=str),
		"UId": request.args.get("userId",None,type=int),
		"EmpId": request.args.get("empId",None,type=int)
	}

	arg_data["withPassword"] = 1
	data = get_rp_accs(**arg_data)

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "Rp_acc",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)

	return response


@api.route("/tbl-dk-rp-accs/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_rp_accs():
	if request.method == 'GET':
		arg_data = {
			"DivId": request.args.get("DivId",None,type=int),
			"DivGuid": request.args.get("DivGuid",None,type=str),
			"notDivId": request.args.get("notDivId",None,type=int),
			"synchDateTime": request.args.get("synchDateTime",None,type=str),
			"RpAccId": request.args.get("id",None,type=int),
			"RpAccRegNo": request.args.get("regNo","",type=str),
			"RpAccName": request.args.get("name","",type=str),
			"UId": request.args.get("userId",None,type=int),
			"EmpId": request.args.get("empId",None,type=int)
		}

		arg_data["withPassword"] = 1
		data = get_rp_accs(**arg_data)

		res = {
			"status": 1 if len(data) > 0 else 0,
			"message": "Rp_acc",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()

		divisions = Division.query\
			.filter_by(GCRecord = None)\
			.filter(Division.DivGuid != None).all()
		companies = Company.query\
			.filter_by(GCRecord = None)\
			.filter(Company.CGuid != None).all()
		users = User.query\
			.filter_by(GCRecord = None)\
			.filter(User.UGuid != None).all()


		division_DivId_list = [division.DivId for division in divisions]
		division_DivGuid_list = [str(division.DivGuid) for division in divisions]

		company_CId_list = [company.CId for company in companies]
		company_CGuid_list = [str(company.CGuid) for company in companies]

		users_UId_list = [user.UId for user in users]
		users_UGuid_list = [str(user.UGuid) for user in users]

		data = []
		failed_data = [] 

		for rp_acc_req in req:
			rp_acc_info = addRpAccDict(rp_acc_req)
			try:
				RpAccRegNo = rp_acc_info["RpAccRegNo"]
				RpAccGuid = rp_acc_info["RpAccGuid"]
				DivGuid = rp_acc_req["DivGuid"]
				CGuid = rp_acc_req["CGuid"]
				UGuid = rp_acc_req["UGuid"]

				try:
					indexed_div_id = division_DivId_list[division_DivGuid_list.index(DivGuid)]
					DivId = int(indexed_div_id)
				except:
					DivId = None
				try:
					indexed_c_id = company_CId_list[company_CGuid_list.index(CGuid)]
					CId = int(indexed_c_id)
				except:
					CId = None
				try:
					indexed_u_id = users_UId_list[users_UGuid_list.index(UGuid)]
					UId = int(indexed_u_id)
				except:
					UId = None

				rp_acc_info["DivId"] = DivId
				rp_acc_info["CId"] = CId
				rp_acc_info["UId"] = UId

				thisRpAcc = Rp_acc.query\
					.filter_by(
						RpAccGuid = RpAccGuid,
						GCRecord = None)\
					.first()

				if thisRpAcc:
					if (thisRpAcc.ModifiedDate < dateutil.parser.parse(rp_acc_info["ModifiedDate"])):
						rp_acc_info["RpAccId"] = thisRpAcc.RpAccId
						thisRpAcc.update(**rp_acc_info)
				else:
					thisRpAcc = Rp_acc(**rp_acc_info)
					db.session.add(thisRpAcc)

				db.session.commit()
				rp_acc_trans_total_req = rp_acc_req["RpAccTransTotal"]

				try:
					RpAccId = thisRpAcc.RpAccId
					rp_acc_trans_total = addRpAccTrTotDict(rp_acc_trans_total_req)
					rp_acc_trans_total["RpAccTrTotId"] = None
					rp_acc_trans_total["RpAccId"] = RpAccId

					thisRpAccTrTotal = Rp_acc_trans_total.query\
						.filter_by(RpAccId = RpAccId, GCRecord = None)\
						.first()
					if thisRpAccTrTotal:
						rp_acc_trans_total["RpAccTrTotId"] = thisRpAccTrTotal.RpAccTrTotId
						thisRpAccTrTotal.update(**rp_acc_trans_total)
					else:
						thisRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
						db.session.add(thisRpAccTrTotal)

					data.append(rp_acc_req)

				except Exception as ex:
					print(f"{datetime.now()} | Rp_acc Api Rp_acc_total Exception: {ex}")

				db.session.commit()

			except Exception as ex:
				print(f"{datetime.now()} | Rp_acc Api Exception: {ex}")
				failed_data.append(rp_acc_req)

		status = checkApiResponseStatus(data, failed_data)

		res = {
			"data": data,
			"fails": failed_data,
			"success_total": len(data),
			"fail_total": len(failed_data)
		}

		for e in status:
			res[e] = status[e]

		status_code = 201 if len(data) > 0 else 200
		response = make_response(jsonify(res), status_code)

	return response