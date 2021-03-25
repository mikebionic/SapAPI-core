# -*- coding: utf-8 -*-
from datetime import datetime
import dateutil.parser

from main_pack import db
from main_pack.api.common import (
	get_division_id_guid_list,
	get_user_id_guid_list,
	get_company_id_guid_list,
)
from main_pack.base import get_id_from_list_indexing
from main_pack.models.users.models import Rp_acc
from main_pack.models.commerce.models import Rp_acc_trans_total
from .add_Rp_acc_dict import add_Rp_acc_dict
from .add_Rp_acc_tr_tot_dict import add_Rp_acc_tr_tot_dict


def save_rp_acc_synch_data(req):

	DivId_list, DivGuid_list = get_division_id_guid_list()
	UId_list, UGuid_list = get_user_id_guid_list()
	CId_list, CGuid_list = get_company_id_guid_list()

	data, fails = [], []
	for rp_acc_req in req:
		try:
			rp_acc_info = add_Rp_acc_dict(rp_acc_req)
			
			RpAccRegNo = rp_acc_info["RpAccRegNo"]
			RpAccGuid = rp_acc_info["RpAccGuid"]

			DivId = get_id_from_list_indexing(DivId_list, DivGuid_list, rp_acc_req["DivGuid"])
			UId = get_id_from_list_indexing(UId_list, UGuid_list, rp_acc_req["UGuid"])
			CId = get_id_from_list_indexing(CId_list, CGuid_list, rp_acc_req["CGuid"])

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
				rp_acc_trans_total = add_Rp_acc_tr_tot_dict(rp_acc_trans_total_req)
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

		except Exception as ex:
			print(f"{datetime.now()} | Rp_acc Api Exception: {ex}")
			fails.append(rp_acc_req)

	db.session.commit()

	return data, fails
