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

def fileToURL(file_type=None,category=None,file_size='undefined',file_name=''):
	try:
		if file_type==None:
			fileUrl = url_for('commerce_api.get_image',image_size=file_size,image_name=file_name)
		elif file_type=='icon':
			fileUrl = url_for('commerce_api.get_icon',category=category,file_name=file_name)
		else:
			fileUrl = url_for('commerce_api.get_image_test',file_type=file_type,file_name=file_name,file_size=file_size)
	except:
		fileUrl = None
	return fileUrl

