from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.commerce import api
from main_pack.base.apiMethods import checkApiResponseStatus

from main_pack.models.commerce.models import Res_price
from main_pack.api.commerce.utils import addResPriceDict
from main_pack import db
from flask import current_app
from main_pack.api.auth.api_login import sha_required


@api.route("/tbl-dk-res-prices/",methods=['GET','POST','PUT'])
@sha_required
def api_res_prices():
	if request.method == 'GET':
		res_prices = Res_price.query\
			.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
		res = {
			"status": 1,
			"message": "All res prices",
			"data": [res_price.to_json_api() for res_price in res_prices],
			"total": len(res_prices)
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
			res_prices = []
			failed_res_prices = [] 
			for res_price in req:
				res_price = addResPriceDict(res_price)
				try:
					if not 'ResPriceId' in res_price:
						newResPrice = Res_price(**res_price)
						db.session.add(newResPrice)
						db.session.commit()
						res_prices.append(res_price)
					else:
						ResPriceId = res_price['ResPriceId']
						thisResPrice = Res_price.query.get(int(ResPriceId))
						if thisResPrice is not None:
							thisResPrice.update(**res_price)
							db.session.commit()
							res_prices.append(res_price)

						else:
							newResPrice = Res_price(**res_price)
							db.session.add(newResPrice)
							db.session.commit()
							res_prices.append(res_price)
				except Exception as ex:
					print(ex)
					failed_res_prices.append(res_price)

			status = checkApiResponseStatus(res_prices,failed_res_prices)
			res = {
				"data": res_prices,
				"fails": failed_res_prices,
				"success_total": len(res_prices),
				"fail_total": len(failed_res_prices)
			}
			for e in status:
				res[e]=status[e]
			response = make_response(jsonify(res),200)
			
	return response