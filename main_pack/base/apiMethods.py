# # Methods used in api building	

def checkApiResponseStatus(success_list,fail_list):
	if(len(success_list)>0 and len(fail_list)>0):
		return 2
	elif(len(success_list)==0 and len(fail_list)>0):
		return 0
	else:
		return 1