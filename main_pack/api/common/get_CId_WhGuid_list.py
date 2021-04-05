from main_pack.models import Division

def get_CId_WhGuid_list():
	divisions = Division.query\
		.filter_by(GCRecord = None)\
		.filter(Division.DivGuid != None).all()

	division_DivGuid_list = [str(division.DivGuid) for division in divisions]
	division_CId_list = [str(division.CId) for division in divisions]

	return division_CId_list, division_DivGuid_list