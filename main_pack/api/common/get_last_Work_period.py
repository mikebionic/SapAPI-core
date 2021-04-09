from main_pack.models import Work_period


def get_last_Work_period():
	data = Work_period.query\
		.filter_by(GCRecord = None, WpIsDefault = True)\
		.first()

	return data