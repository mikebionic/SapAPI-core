from main_pack.models import User

def get_company_id_guid_list():
	users = User.query\
		.filter_by(GCRecord = None)\
		.filter(User.UGuid != None).all()

	users_UId_list = [user.UId for user in users]
	users_UGuid_list = [str(user.UGuid) for user in users]

	return users_UId_list, users_UGuid_list