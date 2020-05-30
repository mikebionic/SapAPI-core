# # Methods used in api building	

def checkApiResponseStatus(success_list,fail_list):
	if(len(success_list)>0 and len(fail_list)>0):
		return {
			"status":2,
			"message":"Success and fail"
			}
	elif(len(success_list)==0 and len(fail_list)>0):
		return {
			"status":0,
			"message":"Fail"
			}
	else:
		return {
			"status":1,
			"message":"Success"
			}