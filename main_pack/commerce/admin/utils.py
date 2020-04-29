def addCategoryDict(req):
	ResOwnerCatId = req.get('ownerCategory')
	ResCatName = req.get('categoryName')
	ResCatDesc = req.get('categoryDesc')
	ResCatIconName = req.get('categoryIcon')
	category = {
		'ResOwnerCatId':ResOwnerCatId,
		'ResCatName':ResCatName,
		'ResCatDesc':ResCatDesc,
		'ResCatIconName':ResCatIconName
	}
	category = configureNulls(category)
	return category

# category_fields = ['ownerCategory','categoryName','categoryDesc','categoryIcon']

def addCompanyInfoDict(req):
	CName = req.get('companyName')
	CFullName = req.get('companyFullName')
	CDesc = req.get('companyDesc')
	AccInfId = req.get('companyAccInfId') # ??
	CAddress = req.get('companyAddress')
	CAddressLegal = req.get('companyAddressLegal')
	CLatitude = req.get('companyLatitude') 
	CLongitude = req.get('companyLongitude') 
	Phone1 = req.get('companyPhone1')
	Phone2 = req.get('companyPhone2')
	Phone3 = req.get('companyPhone3')
	Phone4 = req.get('companyPhone4')
	CPostalCode = req.get('companyPostalCode')
	CEmail = req.get('companyEmail')
	CWTime = req.get('companyWTime')
	companyInfo = {
		'CName':CName,
		'CFullName':CFullName,
		'CDesc':CDesc,
		'AccInfId':AccInfId,
		'CAddress':CAddress,
		'CAddressLegal':CAddressLegal,
		'CLatitude':CLatitude,
		'CLongitude':CLongitude,
		'Phone1':Phone1,
		'Phone2':Phone2,
		'Phone3':Phone3,
		'Phone4':Phone4,
		'CPostalCode':CPostalCode,
		'CEmail':CEmail,
		'CWTime':CWTime
	}
	return companyInfo

# companyInfo_fields = ['companyName','companyFullName','companyDesc','companyAccInfId',
# 		'companyAddress','companyAddressLegal','companyLatitude','companyLongitude',
# 		'companyPhone1','companyPhone2','companyPhone3','companyPhone4',
# 		'companyPostalCode','companyEmail','companyWTime']
############ useful methods ############# 
def boolCheck(value):
	if value == 'False' or value == 'false' or value == '0' or value == 0:
		value = False
	elif value: 
		value = True
	else:
		value = False
	return value
	print(value)

def dateDataCheck(date):
	try:
		date = datetime.strptime(date, "%Y-%m-%d")
	except:
		date = None
	return date

def configureNulls(data):
	for e in data:
		if data[e] == '':
			data[e] = None
	return data

def prepare_data(dropdown,page,title):
	template_data={
		'dropdown': dropdown,
		'page': page,
		'title': title,
	}
	return template_data