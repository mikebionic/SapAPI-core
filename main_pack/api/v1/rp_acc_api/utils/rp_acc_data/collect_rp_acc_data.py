from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import dateutil.parser

from main_pack.models import Division
from main_pack.models import Rp_acc
from main_pack.base.apiMethods import fileToURL


def collect_rp_acc_data(
	DivId = None,
	DivGuid = None,
	notDivId = None,
	synchDateTime = None,
	RpAccId = None,
	RpAccRegNo = None,
	RpAccName = None,
	UId = None,
	EmpId = None,
	withPassword = 0,
):

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

