# # Methods used in api building  
from flask import url_for,send_file
from flask import current_app
import os

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

def fileToURL(path):
	# I want to return url but didn't succeed yet
	if path:
		# print(send_file(os.path.join(current_app.root_path,'static',path)))
		# return os.path.join(current_app.root_path,'static',path)
		return url_for('static',filename=path)
	# except:
	# 	return None