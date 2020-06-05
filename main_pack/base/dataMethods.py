
############ useful methods ############# 
def configureFloat(value):
	try:
		value = float(value)
	except:
		value = 0
	return value

def boolCheck(value):
	if value == 'False' or value == 'false' or value == '0' or value == 0:
		value = False
	elif value:
		value = True
	else:
		value = False
	return value

def dateDataCheck(date):
	try:
		date = datetime.strptime(date, "%Y-%m-%d")
	except:
		date = None
	return date

def apiDataFormat(date):
	try:
		date = date.strftime("%Y-%m-%d %H:%M:%S")
	except:
		date = None
	return date

def configureNulls(data):
	for e in data:
		if data[e] == '' or data[e] == 0:
			data[e] = None
	return data

def prepare_data(dropdown,page,title):
	template_data={
		'dropdown': dropdown,
		'page': page,
		'title': title,
	}
	return template_data