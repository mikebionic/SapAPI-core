# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack import db
from main_pack.api.commerce import api


from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.api.auth.api_login import sha_required

# Users, Rp_accs and functions
from main_pack.models.users.models import Rp_acc,Users
from main_pack.api.users.utils import addRpAccDict,apiRpAccData
# / Users, Rp_accs and functions /

# Rp_acc_trans_total and functions
from main_pack.models.commerce.models import Rp_acc_trans_total
from main_pack.api.commerce.utils import addRpAccTrTotDict
# / Rp_acc_trans_total and functions /

from main_pack.models.base.models import Company, Division


@api.route("/tbl-dk-rp-accs/<RpAccRegNo>/",methods=['GET'])
# @sha_required
def api_rp_accs_rp_acc(RpAccRegNo):
	rp_acc = apiRpAccData(RpAccRegNo)
	res = {
		"status": 1,
		"message": "Single rp_acc",
		"data": rp_acc['data'],
		"total": 1
	}
	response = make_response(jsonify(res),200)

	return response


@api.route("/tbl-dk-rp-accs/",methods=['GET','POST'])
@sha_required
def api_rp_accs():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		DivGuid = request.args.get("DivGuid",None,type=str)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		rp_accs = Rp_acc.query.filter_by(GCRecord = None)\
			.options(
				joinedload(Rp_acc.division),
				joinedload(Rp_acc.company),
				joinedload(Rp_acc.users))
		if DivId:
			rp_accs = rp_accs.filter_by(DivId = DivId)
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
			rp_acc_info["DivGuid"] = rp_acc.division.DivGuid if rp_acc.division else None
			rp_acc_info["CGuid"] = rp_acc.company.CGuid if rp_acc.company else None
			rp_acc_info["UGuid"] = rp_acc.users.UGuid if rp_acc.users else None
			trans_total = [rp_acc_trans_total.to_json_api() 
			for rp_acc_trans_total in rp_acc.Rp_acc_trans_total 
			if rp_acc_trans_total.GCRecord == None]
			
			total_info = trans_total[0] if trans_total else {}
			rp_acc_info["RpAccTransTotal"] = total_info
			trans_total = None
			data.append(rp_acc_info)

		res = {
			"status": 1,
			"message": "Rp_acc",
			"data": data,
			"total": len(rp_accs)
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

			divisions = Division.query\
				.filter_by(GCRecord = None)\
				.filter(Division.DivGuid != None).all()
			companies = Company.query\
				.filter_by(GCRecord = None)\
				.filter(Company.CGuid != None).all()
			users = Users.query\
				.filter_by(GCRecord = None)\
				.filter(Users.UGuid != None).all()


			division_DivId_list = [division.DivId for division in divisions]
			division_DivGuid_list = [str(division.DivGuid) for division in divisions]

			company_CId_list = [company.CId for company in companies]
			company_CGuid_list = [str(company.CGuid) for company in companies]

			users_UId_list = [user.UId for user in users]
			users_UGuid_list = [str(user.UGuid) for user in users]

			rp_accs = []
			failed_rp_accs = [] 
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
					# RpAccRegNo = RpAccRegNo,

					if thisRpAcc:
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
						rp_acc_trans_total['RpAccTrTotId'] = None
						rp_acc_trans_total['RpAccId'] = RpAccId
						thisRpAccTrTotal = Rp_acc_trans_total.query\
							.filter_by(RpAccId = RpAccId, GCRecord = None)\
							.first()
						if thisRpAccTrTotal:
							rp_acc_trans_total['RpAccTrTotId'] = thisRpAccTrTotal.RpAccTrTotId
							thisRpAccTrTotal.update(**rp_acc_trans_total)
						else:
							thisRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
							db.session.add(thisRpAccTrTotal)
						rp_accs.append(rp_acc_req)
					except Exception as ex:
						print(f"{datetime.now()} | Rp_acc Api Rp_acc_total Exception: {ex}")
				except Exception as ex:
					print(f"{datetime.now()} | Rp_acc Api Exception: {ex}")
					failed_rp_accs.append(rp_acc_req)
			db.session.commit()

			status = checkApiResponseStatus(rp_accs,failed_rp_accs)
			res = {
				"data": rp_accs,
				"fails": failed_rp_accs,
				"success_total": len(rp_accs),
				"fail_total": len(failed_rp_accs)
			}		
			for e in status:
				res[e] = status[e]
			response = make_response(jsonify(res),201)
	return response
