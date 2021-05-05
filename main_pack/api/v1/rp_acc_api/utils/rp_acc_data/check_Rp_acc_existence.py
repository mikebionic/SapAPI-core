
from main_pack.models import Rp_acc

def check_Rp_acc_existence(req):

	filtering = {"GCRecord": None}

	data = {}

	if "RpAccGuid" in req:
		filtering["RpAccGuid"] = req["RpAccGuid"]

	if "RpAccRegNo" in req:
		filtering["RpAccRegNo"] = req["RpAccRegNo"]

	if "RpAccUName" in req:
		filtering["RpAccUName"] = req["RpAccUName"]

	if "RpAccName" in req:
		filtering["RpAccName"] = req["RpAccName"]

	if "RpAccEMail" in req:
		filtering["RpAccEMail"] = req["RpAccEMail"]

	if "RpAccMobilePhoneNumber" in req:
		filtering["RpAccMobilePhoneNumber"] = req["RpAccMobilePhoneNumber"]

	rp_acc = Rp_acc.query.filter_by(**filtering).first()
	if rp_acc:
		data = rp_acc.to_json_api()

	return data