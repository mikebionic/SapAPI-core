from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Rp_acc_trans_total
from main_pack.api.commerce.utils import addRpAccTrTotDict
from main_pack import db
from flask import current_app

@api.route("/tbl-dk-rp-acc-trans-totals/",methods=['GET','POST'])
def api_rp_acc_trans_totals():
	if request.method == 'GET':
		rp_acc_trans_totals = Rp_acc_trans_total.query\
			.filter(Rp_acc_trans_total.GCRecord=='' or Rp_acc_trans_total.GCRecord==None).all()
		res = {
			"status":1,
			"message":"All rp acc trans totals",
			"data":[rp_acc_trans_total.to_json_api() for rp_acc_trans_total in rp_acc_trans_totals],
			"total":len(rp_acc_trans_totals)
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
			rp_acc_trans_totals = []
			failed_rp_acc_trans_totals = [] 
			for rp_acc_trans_total in req:
				rp_acc_trans_total = addRpAccTrTotDict(rp_acc_trans_total)
				try:
					if not 'RpAccTrTotId' in rp_acc_trans_total:
						newRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
						db.session.add(newRpAccTrTotal)
						db.session.commit()
						rp_acc_trans_totals.append(rp_acc_trans_total)
					else:
						RpAccTrTotId = rp_acc_trans_total['RpAccTrTotId']
						thisRpAccTrTotal = Rp_acc_trans_total.query.get(int(RpAccTrTotId))
						if thisRpAccTrTotal is not None:
							thisRpAccTrTotal.update(**rp_acc_trans_total)
							db.session.commit()
							rp_acc_trans_totals.append(rp_acc_trans_total)

						else:
							newRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
							db.session.add(newRpAccTrTotal)
							db.session.commit()
							rp_acc_trans_totals.append(rp_acc_trans_total)
				except:
					failed_rp_acc_trans_totals.append(rp_acc_trans_total)

			status = checkApiResponseStatus(rp_acc_trans_totals,failed_rp_acc_trans_totals)
			res = {
				"data":rp_acc_trans_totals,
				"fails":failed_rp_acc_trans_totals,
				"success_total":len(rp_acc_trans_totals),
				"fail_total":len(failed_rp_acc_trans_totals)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)

	return response