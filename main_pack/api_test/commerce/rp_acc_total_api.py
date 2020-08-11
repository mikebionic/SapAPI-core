from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api_test.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models_test.commerce.models import Rp_acc_trans_total
from main_pack.models_test.users.models import Rp_acc
from main_pack.api_test.commerce.utils import addRpAccTrTotDict
from main_pack import db_test
from flask import current_app
from main_pack.api_test.auth.api_login import sha_required

@api.route("/tbl-dk-rp-acc-trans-totals/",methods=['GET','POST'])
@sha_required
def api_rp_acc_trans_totals():
	if request.method == 'GET':
		rp_acc_trans_totals = Rp_acc_trans_total.query.filter_by(GCRecord = None).all()
		res = {
			"status": 1,
			"message": "All rp acc trans totals",
			"data": [rp_acc_trans_total.to_json_api() for rp_acc_trans_total in rp_acc_trans_totals],
			"total": len(rp_acc_trans_totals)
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
			rp_accs = Rp_acc.query\
				.filter_by(GCRecord = None)\
				.all()
			req = request.get_json()
			print(req)
			rp_acc_trans_totals = []
			failed_rp_acc_trans_totals = [] 
			for rp_acc_trans_total in req:
				try:
					RpAccRegNo = rp_acc_trans_total['RpAccRegNo'] 
					rp_acc_trans_total = addRpAccTrTotDict(rp_acc_trans_total)
					rp_acc_list = [rp_acc.to_json_api() for rp_acc in rp_accs if rp_acc.RpAccRegNo == RpAccRegNo]
					if rp_acc_list:
						RpAccId = rp_acc_list[0]['RpAccId']
						rp_acc_trans_total['RpAccId'] = RpAccId
						thisRpAccTrTotal = Rp_acc_trans_total.query\
							.filter_by(RpAccId = RpAccId)\
							.first()
						if thisRpAccTrTotal is not None:
							thisRpAccTrTotal.update(**rp_acc_trans_total)
							db_test.session.commit()
							rp_acc_trans_totals.append(rp_acc_trans_total)
							print('updated tr total')
						else:
							newRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
							db_test.session.add(newRpAccTrTotal)
							db_test.session.commit()
							print('created tr total')
							rp_acc_trans_totals.append(rp_acc_trans_total)
					else:
						raise Exception
				except Exception as ex:
					print(ex)
					failed_rp_acc_trans_totals.append(rp_acc_trans_total)

			status = checkApiResponseStatus(rp_acc_trans_totals,failed_rp_acc_trans_totals)
			res = {
				"data": rp_acc_trans_totals,
				"fails": failed_rp_acc_trans_totals,
				"success_total": len(rp_acc_trans_totals),
				"fail_total": len(failed_rp_acc_trans_totals)
			}
			for e in status:
				res[e]=status[e]
			print(res)
			response = make_response(jsonify(res),200)

	return response
