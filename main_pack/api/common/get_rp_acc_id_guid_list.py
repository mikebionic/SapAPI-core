from main_pack.models import Rp_acc

def get_rp_acc_id_guid_list():
	rp_accs = Rp_acc.query\
		.with_entities(Rp_acc.RpAccId,Rp_acc.RpAccGuid)\
		.filter_by(GCRecord = None)\
		.filter(Rp_acc.RpAccGuid != None).all()
	
	rp_acc_RpAccId_list = [rp_acc.RpAccId for rp_acc in rp_accs]
	rp_acc_RpAccGuid_list = [str(rp_acc.RpAccGuid) for rp_acc in rp_accs]
	return rp_acc_RpAccId_list, rp_acc_RpAccGuid_list