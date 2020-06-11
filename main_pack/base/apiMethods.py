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

def fileToURL(size,name):
	if size and name:
		try:
			fileUrl = url_for('commerce_api.get_image',image_size=size,image_name=name)
		except:
			fileUrl = None
		return fileUrl