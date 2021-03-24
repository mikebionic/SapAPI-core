from main_pack.models.users.models import Users

def get_company_id_guid_list():
	users = Users.query\
		.filter_by(GCRecord = None)\
		.filter(Users.UGuid != None).all()

	users_UId_list = [user.UId for user in users]
	users_UGuid_list = [str(user.UGuid) for user in users]

	return users_UId_list, users_UGuid_list