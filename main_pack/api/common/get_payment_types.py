from main_pack.models import Payment_type

def get_payment_types():
	payment_types = Payment_type.query\
	.filter_by(GCRecord = None)\
	.filter(Payment_type.PtVisibleIndex != 0)\
	.order_by(Payment_type.PtVisibleIndex.asc())\
	.all()

	data = [payment_type.to_json_api() for payment_type in payment_types if payment_type.PtVisibleIndex != 0]
	return data