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