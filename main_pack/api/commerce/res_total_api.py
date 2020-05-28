from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Res_total
from main_pack.api.commerce.utils import addResTotalDict
from main_pack import db
from flask import current_app


@api.route("/res_totals/",methods=['GET','POST','PUT'])
def api_res_totals():
	if request.method == 'GET':
		res_totals = Res_total.query.all()
		res = {
			"status":1,
			"message":"All res totals",
			"data":[res_total.to_json_api() for res_total in res_totals],
			"total":len(res_totals)
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
			res_totals = []
			failed_res_totals = [] 
			for res_total in req:
				res_total = addResTotalDict(res_total)
				try:
					if not 'ResTotId' in res_total:
						newResTotal = Res_total(**res_total)
						db.session.add(newResTotal)
						db.session.commit()
						res_totals.append(res_total)
					else:
						ResTotId = res_total['ResTotId']
						thisResTotal = Res_total.query.get(int(ResTotId))
						if thisResTotal is not None:
							thisResTotal.update(**res_total)
							db.session.commit()
							res_totals.append(res_total)

						else:
							newResTotal = Res_total(**res_total)
							db.session.add(newResTotal)
							db.session.commit()
							res_totals.append(res_total)
				except:
					failed_res_totals.append(res_total)

			status = checkApiResponseStatus(res_totals,failed_res_totals)
			res = {
				"status": status,
				"message":"Res totals added",
				"data":res_totals,
				"fails":failed_res_totals,
				"success_total":len(res_totals),
				"fail_total":len(failed_res_totals)
			}

			response = make_response(jsonify(res),200)
			print(response)

	return response