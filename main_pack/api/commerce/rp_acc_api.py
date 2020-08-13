from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.users.models import Rp_acc
from main_pack.api.users.utils import addRpAccDict,apiRpAccData
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required

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
		rp_accs = Rp_acc.query.filter_by(GCRecord = None).all()
		res = {
			"status": 1,
			"message": "All rp_accs",
			"data": [rp_acc.to_json_api() for rp_acc in rp_accs],
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
			print(req)
			rp_accs = []
			failed_rp_accs = [] 
			for rp_acc in req:
				rp_acc = addRpAccDict(rp_acc)				
				try:
					RpAccRegNo = rp_acc['RpAccRegNo']
					RpAccName = rp_acc['RpAccName']
					thisRpAcc = Rp_acc.query\
						.filter_by(RpAccRegNo = RpAccRegNo, RpAccName = RpAccName)\
						.first()
					if thisRpAcc:
						thisRpAcc.update(**rp_acc)
						db.session.commit()
						rp_accs.append(rp_acc)
					else:
						newRpAcc = Rp_acc(**rp_acc)
						db.session.add(newRpAcc)
						db.session.commit()
						rp_accs.append(rp_acc)
				except Exception as ex:
					print(ex)
					failed_rp_accs.append(rp_acc)

			status = checkApiResponseStatus(rp_accs,failed_rp_accs)
			res = {
				"data": rp_accs,
				"fails": failed_rp_accs,
				"success_total": len(rp_accs),
				"fail_total": len(failed_rp_accs)
			}		
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),201)
	return response 