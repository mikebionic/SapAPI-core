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


# import os
# if not os.path.exists('work/'):
# 	try:
# 		os.makedirs('work/')
# 	except:
# 		print("error creating directory")

# import os, secrets
# from flask import current_app
# from PIL import Image



# def get_path(form_image,module,id):
# 	random_hex = secrets.token_hex(14)
# 	_, f_ext = os.path.splitext(form_image.filename)
# 	image_fn = random_hex + f_ext
# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)
# 	# original quality
# 	form_image.save(image_path)

# 	return form_image, image_path, image_fn


# def save_image(form_image,module,id):
# 	random_hex = secrets.token_hex(14)
# 	_, f_ext = os.path.splitext(form_image.filename)
# 	image_fn = random_hex + f_ext
# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)
# 	# original quality
# 	form_image.save(image_path)

# 	size_s = (150,150)
# 	size_m = (300,300)
# 	size_l = (1280,1280)


# 	i = Image.open(form_image)
# 	i.thumbnail(output_size)
# 	i.save(image_path)
# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)


# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)


# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)
# 	# for getting direct path after static folder to store in DB
# 	path = os.path.join(path,image_fn)
# 	return {"FileName":image_fn,"FilePath":path}



# def saveImageQuality(form_image,size,image_path)
# 	output_sizes = {
# 		"xdpi":(150,150),
# 		"xxdpi":(300,300),
# 		"xxxdpi":(1280,1280)
# 	}
# 	i = Image.open(form_image)
# 	i.thumbnail(output_size)
# 	i.save(image_path)
# 	image_path = os.path.join(current_app.root_path,'static/',module,id,'images/',size,picture_fn)





# img = save_image(form.picture.data,"commerce/users",UId)