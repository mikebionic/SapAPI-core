# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from flask import current_app
from datetime import datetime, timedelta
import dateutil.parser

from main_pack import db
from . import api
from .utils import addRpAccTrTotDict

from main_pack.models import Rp_acc_trans_total
from main_pack.models import Rp_acc

from main_pack.api.auth.utils import sha_required
from main_pack.api.base.validators import request_is_json
from main_pack.base.apiMethods import checkApiResponseStatus


@api.route("/tbl-dk-rp-acc-trans-totals/",methods=['GET','POST'])
@sha_required
@request_is_json(request)
def api_rp_acc_trans_totals():
	if request.method == 'GET':
		DivId = request.args.get("DivId",None,type=int)
		notDivId = request.args.get("notDivId",None,type=int)
		synchDateTime = request.args.get("synchDateTime",None,type=str)

		rp_acc_trans_totals = Rp_acc_trans_total.query.filter_by(GCRecord = None)

		if DivId:
			rp_acc_trans_totals = rp_acc_trans_totals.filter_by(DivId = DivId)

		if notDivId:
			rp_acc_trans_totals = rp_acc_trans_totals.filter(Rp_acc_trans_total.DivId != notDivId)

		if synchDateTime:
			if (type(synchDateTime) != datetime):
				synchDateTime = dateutil.parser.parse(synchDateTime)
			rp_acc_trans_totals = rp_acc_trans_totals.filter(Rp_acc_trans_total.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))

		data = [rp_acc_trans_total.to_json_api() for rp_acc_trans_total in rp_acc_trans_totals.all()]

		res = {
			"status": 1,
			"message": "All rp acc trans totals",
			"data": data,
			"total": len(data)
		}
		response = make_response(jsonify(res), 200)

	elif request.method == 'POST':
		req = request.get_json()			

		rp_accs = Rp_acc.query.filter_by(GCRecord = None).all()
		rp_acc_list_reg_no = [rp_acc.RpAccRegNo for rp_acc in rp_accs]
		rp_acc_list = [rp_acc.RpAccId for rp_acc in rp_accs]

		data = []
		failed_data = []

		for rp_acc_trans_total_req in req:
			try:
				RpAccRegNo = rp_acc_trans_total_req['RpAccRegNo']
				rp_acc_trans_total = addRpAccTrTotDict(rp_acc_trans_total_req)
				rp_acc_id = rp_acc_list[rp_acc_list_reg_no.index(RpAccRegNo)]

				if rp_acc_id:
					RpAccId = int(rp_acc_id)
					rp_acc_trans_total['RpAccId'] = RpAccId
					thisRpAccTrTotal = Rp_acc_trans_total.query\
						.filter_by(RpAccId = RpAccId)\
						.first()
					if thisRpAccTrTotal is not None:
						thisRpAccTrTotal.update(**rp_acc_trans_total)
						data.append(rp_acc_trans_total)
					else:
						newRpAccTrTotal = Rp_acc_trans_total(**rp_acc_trans_total)
						db.session.add(newRpAccTrTotal)
						data.append(rp_acc_trans_total)
				else:
					raise Exception

			except Exception as ex:
				print(f"{datetime.now()} | Rp_acc_total Api Exception: {ex}")
				failed_data.append(rp_acc_trans_total)

		db.session.commit()
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