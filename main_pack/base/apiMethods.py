# # Methods used in api building  
from flask import url_for,send_file
from flask import current_app
import os

def checkApiResponseStatus(success_list,fail_list):
	if(len(success_list)>0 and len(fail_list)>0):
		return {
			"status": 2,
			"message": "Success and fail"
			}
	elif(len(success_list)==0 and len(fail_list)>0):
		return {
			"status": 0,
			"message": "Fail"
			}
	else:
		return {
			"status": 1,
			"message": "Success"
			}

def fileToURL(file_type=None,category=None,file_size='undefined',file_name='',url=None):
	try:
		if file_type=='icon':
			if url:
				url = url
			else:
				url = 'commerce_api.get_icon'
			fileUrl = url_for(url,category=category,file_name=file_name)
		else:
			if url:
				url = url
			else:
				url = 'commerce_api.get_image'
			fileUrl = url_for(url,file_type=file_type,file_size=file_size,file_name=file_name)
	except Exception as ex:
		fileUrl = None
	return fileUrl