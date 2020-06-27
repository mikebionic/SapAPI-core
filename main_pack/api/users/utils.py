from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck

def addUsersDict(req):
	UId = req.get('UId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	RpAccId = req.get('RpAccId')
	UFullName = req.get('UFullName')
	UName = req.get('UName')
	UEmail = req.get('UEmail')
	UPass = req.get('UPass')
	UShortName = req.get('UShortName')
	EmpId = req.get('EmpId')
	UTypeId = req.get('UTypeId')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	users = {
		'CId':CId,
		'DivId':DivId,
		'RpAccId':RpAccId,
		'UFullName':UFullName,
		'UName':UName,
		'UEmail':UEmail,
		'UPass':UPass,
		'UShortName':UShortName,
		'EmpId':EmpId,
		'UTypeId':UTypeId,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
		}
	if(UId != '' and UId != None):
		users['UId']=UId
	users=configureNulls(users)
	return users

def addRpAccDict(req):
	RpAccId = req.get('RpAccId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	EmpId = req.get('EmpId')
	GenderId = req.get('GenderId')
	NatId = req.get('NatId')
	RpAccStatusId = req.get('RpAccStatusId')
	ReprId = req.get('ReprId')
	RpAccTypeId = req.get('RpAccTypeId')
	WpId = req.get('WpId')
	RpAccRegNo = req.get('RpAccRegNo')
	RpAccName = req.get('RpAccName')
	RpAccUName = req.get('RpAccUName')
	RpAccUPass = req.get('RpAccUPass')
	RpAccAddress = req.get('RpAccAddress')
	RpAccMobilePhoneNumber = req.get('RpAccMobilePhoneNumber')
	RpAccHomePhoneNumber = req.get('RpAccHomePhoneNumber')
	RpAccWorkPhoneNumber = req.get('RpAccWorkPhoneNumber')
	RpAccWorkFaxNumber = req.get('RpAccWorkFaxNumber')
	RpAccZipCode = req.get('RpAccZipCode')
	RpAccEMail = req.get('RpAccEMail')
	RpAccFirstName = req.get('RpAccFirstName')
	RpAccLastName = req.get('RpAccLastName')
	RpAccPatronomic = req.get('RpAccPatronomic')
	RpAccBirthDate = req.get('RpAccBirthDate')
	RpAccResidency = req.get('RpAccResidency')
	RpAccPassportNo = req.get('RpAccPassportNo')
	RpAccPassportIssuePlace = req.get('RpAccPassportIssuePlace')
	RpAccLangSkills = req.get('RpAccLangSkills')
	RpAccSaleBalanceLimit = req.get('RpAccSaleBalanceLimit')
	RpAccPurchBalanceLimit = req.get('RpAccPurchBalanceLimit')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')
	rp_acc = {		
		'CId':CId,
		'DivId':DivId,
		'EmpId':EmpId,
		'GenderId':GenderId,
		'NatId':NatId,
		'RpAccStatusId':RpAccStatusId,
		'ReprId':ReprId,
		'RpAccTypeId':RpAccTypeId,
		'WpId':WpId,
		'RpAccRegNo':RpAccRegNo,
		'RpAccName':RpAccName,
		'RpAccUName':RpAccUName,
		'RpAccUPass':RpAccUPass,
		'RpAccAddress':RpAccAddress,
		'RpAccMobilePhoneNumber':RpAccMobilePhoneNumber,
		'RpAccHomePhoneNumber':RpAccHomePhoneNumber,
		'RpAccWorkPhoneNumber':RpAccWorkPhoneNumber,
		'RpAccWorkFaxNumber':RpAccWorkFaxNumber,
		'RpAccZipCode':RpAccZipCode,
		'RpAccEMail':RpAccEMail,
		'RpAccFirstName':RpAccFirstName,
		'RpAccLastName':RpAccLastName,
		'RpAccPatronomic':RpAccPatronomic,
		'RpAccBirthDate':RpAccBirthDate,
		'RpAccResidency':RpAccResidency,
		'RpAccPassportNo':RpAccPassportNo,
		'RpAccPassportIssuePlace':RpAccPassportIssuePlace,
		'RpAccLangSkills':RpAccLangSkills,
		'RpAccSaleBalanceLimit':RpAccSaleBalanceLimit,
		'RpAccPurchBalanceLimit':RpAccPurchBalanceLimit,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
		}
	if(RpAccId != '' and RpAccId != None):
		print(RpAccId)
		rp_acc['RpAccId']=RpAccId
	rp_acc = configureNulls(rp_acc)
	return rp_acc

from main_pack.models.base.models import Image
from main_pack.models.commerce.models import Resource
from main_pack.base.apiMethods import fileToURL
from main_pack.models.users.models import Users,Rp_acc,User_type
from sqlalchemy import and_

def apiUsersData(UId):
	user = Users.query\
		.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.UId==UId).first()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()
	# one user - one rp_acc?
	rp_acc = Rp_acc.query\
		.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),Rp_acc.UId==UId).first()

	user_type = User_type.query\
		.filter(and_(User_type.GCRecord=='' or User_type.GCRecord==None),User_type.UTypeId==user.UTypeId).first()
	################
	userList = user.to_json_api()

	userList["Rp_acc"] = rp_acc.to_json_api() if rp_acc else ''
	userList["User_type"] = user_type.to_json_api() if user_type else ''

	List_Images = [image.FileName for image in images if image.UId==user.UId]
	userList["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=List_Images[0]) if List_Images else ''
	userList["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=List_Images[0]) if List_Images else ''
	userList["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=List_Images[0]) if List_Images else ''
	# configure this for uniqueness later on
	imagesList = []
	for imageName in List_Images:
		resImage = {}
		resImage["FilePathS"] = fileToURL(file_type='image',file_size='S',file_name=imageName) if List_Images else ''
		resImage["FilePathM"] = fileToURL(file_type='image',file_size='M',file_name=imageName) if List_Images else ''
		resImage["FilePathR"] = fileToURL(file_type='image',file_size='R',file_name=imageName) if List_Images else ''
		imagesList.append(resImage)
	userList['Images'] = imagesList

	# data.append(userList)
	#############
	res = {
		"status":1,
		"data":userList,
		"total":1
	}
	return res