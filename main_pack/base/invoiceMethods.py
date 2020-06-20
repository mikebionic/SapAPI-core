
invStatSelector = {
	# Waiting
	1:{
		"class":"warning",
		"color_hash":"#eda514", 
		"percentage":10,
		"icon":"loader",
	},
	# Received (not order maybe, discuss with dovlet)
	2:{
		"class":"success",
		"color_hash":"#00b289", 
		"percentage":30,
		"icon":"dollar-sign",
	},
	# Talked with a client
	3:{
		"class":"success",
		"color_hash":"#00b289", 
		"percentage":30,
		"icon":"thumbs-up",
	},
	# Approved
	4:{
		"class":"success",
		"color_hash":"#00b289", 
		"percentage":30,
		"icon":"check",
	},
	# Not approved
	5:{
		"class":"danger",
		"color_hash":"#FF7273", 
		"percentage":30,
		"icon":"x-circle",
	},
	# Collecting goods
	6:{
		"class":"success",
		"color_hash":"#00b289", 
		"percentage":40,
		"icon":"package",
	},
	# Order sent
	7:{
		"class":"info",
		"color_hash":"#63d3fa", 
		"percentage":65,
		"icon":"truck",
	},
	# Transfered to customer
	8:{
		"class":"info",
		"color_hash":"#63d3fa", 
		"percentage":88,
		"icon":"gift",
	},
	# Returned
	9:{
		"class":"danger",
		"color_hash":"#FF7273", 
		"percentage":60,
		"icon":"corner-up-left",
	},
	# Note
	10:{
		"class":"warning",
		"color_hash":"#eda514", 
		"percentage":50,
		"icon":"alert-octagon",
	},
	# Modified
	11:{
		"class":"warning",
		"color_hash":"#eda514", 
		"percentage":60,
		"icon":"edit-2",
	},
	# Complete
	12:{
		"class":"primary",
		"color_hash":"#0023ff", 
		"percentage":100,
		"icon":"award",
	},
}


def getInvStatusUi(statusId):
	try:
		for status in invStatSelector:
			if status == statusId:
				invStatusUi = invStatSelector[status]				
	except:
		invStatusUi = invStatSelector[1]
	return invStatusUi