from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck
from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.apiMethods import fileToURL

from main_pack.models import Image
from main_pack.models import (
	User,
	User_type,
	Rp_acc,
	Rp_acc_type,
	Rp_acc_status
)

from main_pack.models import (
	Unit,
	Brand,
	Usage_status,
	Res_category,
	Res_type,
	Res_maker
)

from main_pack.models import (
	Barcode,
	Res_color,
	Res_size,
	Res_translation,
	Unit,
	Res_unit,
	Res_price,
	Res_total,
	Res_trans_inv_line,
	Res_transaction,
	Rp_acc_resource,
	Sale_agr_res_price,
	Res_discount
)


# !!! TODO: These functions are similar to api/users/utils.py, merge them with respect to api
def UiRpAccData(rp_acc_list=None, dbQuery=None, dbModels=None, deleted=False):
	data = []
	filtering = {}
	if not dbModels:
		dbModels = []	
		if not deleted:
			filtering["GCRecord"] = None
		
		if rp_acc_list is None:
			rp_accs = Rp_acc.query.filter_by(**filtering)\
				.options(
					joinedload(Rp_acc.user),
					joinedload(Rp_acc.rp_acc_status),
					joinedload(Rp_acc.rp_acc_type),
					joinedload(Rp_acc.Image))\
				.all()
			for rp_acc in rp_accs:
				dbModels.append(rp_acc)
		
		else:
			for rp_acc_index in rp_acc_list:
				rp_acc = Rp_acc.query\
					.filter_by(**filtering, RpAccId = rp_acc_index["RpAccId"])\
					.options(
						joinedload(Rp_acc.user),
						joinedload(Rp_acc.rp_acc_status),
						joinedload(Rp_acc.rp_acc_type),
						joinedload(Rp_acc.Image))\
					.first()
				dbModels.append(rp_acc)
	
	for rp_acc in dbModels:
		rpAccInfo = rp_acc.to_json_api()

		# !!! TODO: Check for joinedloading this if relationship
		rp_acc_user = User.query\
			.filter_by(GCRecord = None, RpAccId = rp_acc.RpAccId)\
			.first()
		rp_acc_vendor = rp_acc.user if rp_acc.user and not rp_acc.user.GCRecord else {}

		List_Images = [image.to_json_api() for image in rp_acc.Image if not image.GCRecord]
		List_Images = (sorted(List_Images, key = lambda i: i["ModifiedDate"]))

		rpAccInfo["Rp_acc_status"] = dataLangSelector(rp_acc.rp_acc_status.to_json_api()) if rp_acc.rp_acc_status and not rp_acc.rp_acc_status.GCRecord else {}
		rpAccInfo["Rp_acc_type"] = dataLangSelector(rp_acc.rp_acc_type.to_json_api()) if rp_acc.rp_acc_type and not rp_acc.rp_acc_type.GCRecord else {}
		rpAccInfo["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		rpAccInfo["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		rpAccInfo["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[-1]["FileName"]) if List_Images else ""
		rpAccInfo["Images"] = List_Images if List_Images else []
		
		rpAccInfo["Rp_acc_user"] = rp_acc_user.to_json_api() if rp_acc_user else {}
		rpAccInfo["Rp_acc_vendor"] = rp_acc_vendor.to_json_api() if rp_acc_vendor else {}

		data.append(rpAccInfo)

	res = {
		"rp_accs":data,
	}
	return res


def UiUsersData(users_list=None, deleted=False):
	data = []

	user_types = User_type.query\
		.filter_by(GCRecord = None).all()
	images = Image.query\
		.filter_by(GCRecord = None)\
		.order_by(Image.CreatedDate.desc()).all()
	rp_accs = Rp_acc.query\
		.filter_by(GCRecord = None)\
		.order_by(Rp_acc.CreatedDate.desc()).all()

	users_models = []
	
	if users_list is None:
		if deleted==True:
			users = User.query\
				.filter_by(RpAccId = None).all()
		else:
			users = User.query\
				.filter_by(GCRecord = None, RpAccId = None)\
				.all()
		for user in users:
			users_models.append(user)
	else:
		for users_index in users_list:
			if deleted==True:
				user = User.query\
					.filter_by(UId = users_index["UId"]).first()
			else:
				user = User.query\
					.filter_by(GCRecord = None, UId = users_index["UId"])\
					.first()
			users_models.append(user)
		
	for user in users_models:
		userInfo = user.to_json_api()

		List_User_types = [user_type.to_json_api() for user_type in user_types if user_type.UTypeId==user.UTypeId]
		List_Images = [image.to_json_api() for image in images if image.UId==user.UId]
		List_Rp_accs = [rp_acc.to_json_api() for rp_acc in rp_accs if rp_acc.UId==user.UId]

		userInfo["User_type"] = dataLangSelector(List_User_types[0]) if List_User_types else ""
		userInfo["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]["FileName"]) if List_Images else ""
		userInfo["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]["FileName"]) if List_Images else ""
		userInfo["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]["FileName"]) if List_Images else ""
		userInfo["Images"] = List_Images
		userInfo["Rp_accs"] = List_Rp_accs

		data.append(userInfo)
	res = {
		"users": data,
	}
	return res