from main_pack.models import Company

def get_user_id_guid_list():
	companies = Company.query\
		.filter_by(GCRecord = None)\
		.filter(Company.CGuid != None).all()

	company_CId_list = [company.CId for company in companies]
	company_CGuid_list = [str(company.CGuid) for company in companies]

	return company_CId_list, company_CGuid_list