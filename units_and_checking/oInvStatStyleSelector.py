
invStatSelector = {
	# Waiting
	1:{
		"tag_class":"warning",
		"status_color_hash":"#eda514", 
		"status_value":10,
		"status_icon":"loader",
	},
	# Received (not order maybe, discuss with dovlet)
	2:{
		"tag_class":"success",
		"status_color_hash":"#00b28", 
		"status_value":30,
		"status_icon":"dollar-sign",
	},
	# Talked with a client
	3:{
		"tag_class":"success",
		"status_color_hash":"#00b28", 
		"status_value":30,
		"status_icon":"thumbs-up",
	},
	# Approved
	4:{
		"tag_class":"success",
		"status_color_hash":"#00b28", 
		"status_value":30,
		"status_icon":"check",
	},
	# Not approved
	5:{
		"tag_class":"danger",
		"status_color_hash":"#FF7273", 
		"status_value":30,
		"status_icon":"x-circle",
	},
	# Collecting goods
	6:{
		"tag_class":"success",
		"status_color_hash":"#00b28", 
		"status_value":40,
		"status_icon":"package",
	},
	# Order sent
	7:{
		"tag_class":"primary",
		"status_color_hash":"#0023ff", 
		"status_value":65,
		"status_icon":"truck",
	},
	# Transfered to customer
	8:{
		"tag_class":"primary",
		"status_color_hash":"#0023ff", 
		"status_value":88,
		"status_icon":"gift",
	},
	# Returned
	9:{
		"tag_class":"danger",
		"status_color_hash":"#FF7273", 
		"status_value":60,
		"status_icon":"corner-up-left",
	},
	# Note
	10:{
		"tag_class":"warning",
		"status_color_hash":"#eda514", 
		"status_value":50,
		"status_icon":"alert-octagon",
	},
	# Modified
	11:{
		"tag_class":"warning",
		"status_color_hash":"#eda514", 
		"status_value":60,
		"status_icon":"edit-2",
	},
	# Complete
	12:{
		"tag_class":"primary",
		"status_color_hash":"#0023ff", 
		"status_value":100,
		"status_icon":" award",
	},
}

for status in invStatSelector:
	if status == 4:
		print(invStatSelector[status])