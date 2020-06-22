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

def fileToURL(fileType=None,size=None,name=''):
	try:
		if fileType==None:
			fileUrl = url_for('commerce_api.get_image',image_size=size,image_name=name)
		else:
			fileUrl = url_for('commerce_api.get_image_test',fileType=fileType,file_size=size,file_name=name)
			# fileUrl = url_for('commerce_api.get_file',fileType=fileType,fileName=name)
	except:
		fileUrl = None
	return fileUrl

