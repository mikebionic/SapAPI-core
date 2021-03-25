from main_pack.models.base.models import Division

def get_division_id_guid_list():
	divisions = Division.query\
		.filter_by(GCRecord = None)\
		.filter(Division.DivGuid != None).all()

	division_DivId_list = [division.DivId for division in divisions]
	division_DivGuid_list = [str(division.DivGuid) for division in divisions]
	return division_DivId_list, division_DivGuid_list