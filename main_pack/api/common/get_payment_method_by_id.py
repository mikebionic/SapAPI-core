from main_pack.models import Payment_method

def get_payment_method_by_id(PmId):
	try:
		data = Payment_method.query\
			.filter_by(GCRecord = None, PmId = PmId)\
			.filter(Payment_method.PmVisibleIndex != 0)\
			.first()
	except:
		data = None
	
	return data