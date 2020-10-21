# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser
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


@api.route("/tbl-dk-rp-accs/<RpAccRegNo>/",methods=['GET'])
@sha_required
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
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)
		rp_accs = Rp_acc.query.filter_by(GCRecord = None)
		if DivId:
			rp_accs = rp_accs.filter_by(DivId = DivId)
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
			trans_total = [rp_acc_trans_total.to_json_api() for rp_acc_trans_total in rp_acc.Rp_acc_trans_total]
			
			total_info = {}
			if trans_total:
				total_info = trans_total[0]
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

			users = Users.query.filter_by(GCRecord = None).all()
			UId_list = [user.UId for user in users]

			rp_accs = []
			failed_rp_accs = [] 
			for data in req:
				rp_acc = addRpAccDict(data)
				try:
					try:
						user = UId_list.index(rp_acc['UId'])
					except:
						rp_acc['UId'] = None
					RpAccRegNo = rp_acc['RpAccRegNo']
					thisRpAcc = Rp_acc.query\
						.filter_by(RpAccRegNo = RpAccRegNo)\
						.first()

					# !!! Todo add rp_acc guid checkup and // order inv should check rp_accs rp_accId by guid
					if thisRpAcc:
						thisRpAcc.update(**rp_acc)
					else:
						thisRpAcc = Rp_acc(**rp_acc)
						db.session.add(thisRpAcc)

					db.session.commit()

					rp_acc_trans_total = data['RpAccTransTotal']
					try:
						rp_acc_trans_total = addRpAccTrTotDict(rp_acc_trans_total)
						rp_acc_trans_total['RpAccTrTotId'] = None
						RpAccId = thisRpAcc.RpAccId
						rp_acc_trans_total['RpAccId'] = RpAccId
						thisRpAccTrTotal = Rp_acc_trans_total.query\
							.filter_by(RpAccId = RpAccId)\
							.first()
						if thisRpAccTrTotal:
							thisRpAccTrTotal.update(**rp_acc_trans_total)
						else:
							newRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
							db.session.add(newRpAccTrTotal)
						rp_accs.append(rp_acc)
					except Exception as ex:
						print(f"{datetime.now()} | Rp_acc Api Rp_acc_total Exception: {ex}")
				except Exception as ex:
					print(f"{datetime.now()} | Rp_acc Api Exception: {ex}")
					failed_rp_accs.append(rp_acc)
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
