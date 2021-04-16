from main_pack.models import Payment_method

def get_payment_methods():
	payment_methods = Payment_method.query\
		.filter_by(GCRecord = None)\
		.filter(Payment_method.PmVisibleIndex != 0)\
		.order_by(Payment_method.PmVisibleIndex.asc())\
		.all()

	data = [payment_method.to_json_api() for payment_method in payment_methods if payment_method.PmVisibleIndex != 0]

	return data