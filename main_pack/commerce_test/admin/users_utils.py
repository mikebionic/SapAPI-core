from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck

from main_pack.models_test.base.models import Image
# from main_pack.models_test.commerce.models import Resource
from main_pack.base.apiMethods import fileToURL
from main_pack.models_test.users.models import (Users,User_type,
																					Rp_acc,Rp_acc_type,Rp_acc_status)
from sqlalchemy import and_

from main_pack.models_test.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models_test.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,Sale_agr_res_price,Res_discount)

from main_pack.base.languageMethods import dataLangSelector

def UiRpAccData(rp_acc_list=None,deleted=False):
	data = []

	rp_acc_statuses = Rp_acc_status.query\
		.filter(Rp_acc_status.GCRecord=='' or Rp_acc_status.GCRecord==None).all()
	rp_acc_types = Rp_acc_type.query\
		.filter(Rp_acc_type.GCRecord=='' or Rp_acc_type.GCRecord==None).all()

	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None)\
		.order_by(Image.CreatedDate.desc()).all()

	rp_acc_models = []
	
	if rp_acc_list is None:
		if deleted==True:
			rp_accs = Rp_acc.query.all()
		else:
			rp_accs = Rp_acc.query\
				.filter(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None).all()
		for rp_acc in rp_accs:
			rp_acc_models.append(rp_acc)
	else:
		for rp_acc_index in rp_acc_list:
			if deleted==True:
				rp_acc = Rp_acc.query\
					.filter(Rp_acc.RpAccId == rp_acc_index["RpAccId"]).first()
			else:
				rp_acc = Rp_acc.query\
					.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
						Rp_acc.RpAccId == rp_acc_index["RpAccId"]).first()
			rp_acc_models.append(rp_acc)
		
	for rp_acc in rp_acc_models:
		rpAccInfo = rp_acc.to_json_api()

		rp_acc_user = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.RpAccId==rp_acc.RpAccId).first()
		rp_acc_vendor = Users.query\
			.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.UId==rp_acc.UId).first()
		
		List_RpAccStatuses = [rp_acc_status.to_json_api() for rp_acc_status in rp_acc_statuses if rp_acc_status.RpAccStatusId==rp_acc.RpAccStatusId]
		List_RpAccTypes = [rp_acc_type.to_json_api() for rp_acc_type in rp_acc_types if rp_acc_type.RpAccTypeId==rp_acc.RpAccTypeId]
		List_Images = [image.to_json_api() for image in images if image.RpAccId==rp_acc.RpAccId]

		rpAccInfo["Rp_acc_status"] = dataLangSelector(List_RpAccStatuses[0]) if List_RpAccStatuses else ''
		rpAccInfo["Rp_acc_type"] = dataLangSelector(List_RpAccTypes[0]) if List_RpAccTypes else ''
		rpAccInfo["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
		rpAccInfo["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
		rpAccInfo["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''
		rpAccInfo['Images'] = List_Images
		
		rpAccInfo["Rp_acc_user"] = rp_acc_user.to_json_api() if rp_acc_user else ''
		rpAccInfo["Rp_acc_vendor"] = rp_acc_vendor.to_json_api() if rp_acc_vendor else ''

		data.append(rpAccInfo)
	res = {
		"rp_accs":data,
	}
	return res

def UiUsersData(users_list=None,deleted=False):
	data = []

	user_types = User_type.query\
		.filter(User_type.GCRecord=='' or User_type.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None)\
		.order_by(Image.CreatedDate.desc()).all()
	rp_accs = Rp_acc.query\
		.filter(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None)\
		.order_by(Rp_acc.CreatedDate.desc()).all()

	users_models = []
	
	if users_list is None:
		if deleted==True:
			users = Users.query\
				.filter(Users.RpAccId==None).all()
		else:
			users = Users.query\
				.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
					Users.RpAccId==None).all()
		for user in users:
			users_models.append(user)
	else:
		for users_index in users_list:
			if deleted==True:
				user = Users.query\
					.filter(Users.UId == users_index["UId"]).first()
			else:
				user = Users.query\
					.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),\
						Users.UId == users_index["UId"]).first()
			users_models.append(user)
		
	for user in users_models:
		userInfo = user.to_json_api()

		List_User_types = [user_type.to_json_api() for user_type in user_types if user_type.UTypeId==user.UTypeId]
		List_Images = [image.to_json_api() for image in images if image.UId==user.UId]
		List_Rp_accs = [rp_acc.to_json_api() for rp_acc in rp_accs if rp_acc.UId==user.UId]

		userInfo["User_type"] = dataLangSelector(List_User_types[0]) if List_User_types else ''
		userInfo["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]['FileName']) if List_Images else ''
		userInfo["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]['FileName']) if List_Images else ''
		userInfo["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]['FileName']) if List_Images else ''
		userInfo['Images'] = List_Images
		userInfo["Rp_accs"] = List_Rp_accs

		data.append(userInfo)
	res = {
		"users":data,
	}
	return res