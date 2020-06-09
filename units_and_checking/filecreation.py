# in the app use:
# os.path.join(current_app.root_path,'static/',module,id,'images/',picture_fn)

# instead of:
# os.path.join(os.getcwd(),FilePath


#### yet, another working example.... should configure where it's a fileName to open or form_image to process ###
import os
import sys
from PIL import Image
import secrets

def dirHandler(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			print("error creating directory")

def changeImageSize(form_image,modulePath,FileName):
	output_sizes = {
		"R":None,
		"M":(800,600),
		"S":(320,240),
	}
	paths={}
	for size in output_sizes:
		dirHandler(os.path.join(modulePath,size))
		# makes the "module/id/R/blahblah.jpg"
		FilePath = os.path.join(modulePath,size,FileName)
		# join app root path with filepath of image
		# saving_path = os.path.join(current_app.root_path,FilePath)
		saving_path = os.path.join(os.getcwd(),FilePath)
		if not output_sizes[size]:
			form_image.save(saving_path,optimize=True,quality=65)
			paths["FilePath"+size]=FilePath
		else:
			form_image.thumbnail(output_sizes[size])
			form_image.save(saving_path,optimize=True)
			paths["FilePath"+size]=FilePath

	return paths

def save_image(form_image,module,id):
	random_hex = secrets.token_hex(14)
	form_image = Image.open(form_image)
	_, f_ext = os.path.splitext(form_image.filename)
	FileName = random_hex + f_ext

	modulePath = os.path.join('static/',module,str(id),'images')

	resizing = changeImageSize(form_image,modulePath,FileName)
	print(resizing)

save_image('IMG_5660.JPG',"commerce/users",12)

#########################################

########## working example using form inputs #####

# import os
# import sys
# from PIL import Image
# import secrets

# def dirHandler(path):
# 	if not os.path.exists(path):
# 		try:
# 			os.makedirs(path)
# 		except:
# 			print("error creating directory")

# def changeImageSize(FilePath,modulePath,FileName):
# 	output_sizes = {
# 		"M":(800,600),
# 		"S":(320,240),
# 		# "R":None
# 	}
# 	paths={}
# 	for size in output_sizes:
# 		image = Image.open(FilePath)
# 		dirHandler(os.path.join(modulePath,size))
# 		# makes the "module/id/R/blahblah.jpg"
# 		FilePath = os.path.join(modulePath,size,FileName)
# 				# join app root path with filepath of image
# 		# saving_path = os.path.join(current_app.root_path,FilePath)
# 		saving_path = os.path.join(os.getcwd(),FilePath)
# 		if not output_sizes[size]:
# 			image.save(saving_path)
# 			paths["FilePath"+size]=FilePath
# 		else:
# 			image.thumbnail(output_sizes[size])
# 			image.save(saving_path)
# 			paths["FilePath"+size]=FilePath

# 	return paths


# def save_image(form_image=None,savedImage=None,module="undefined",id="undefined"):
# 	if not form_image:
# 		image = Image.open(savedImage)
# 	if form_image:
# 		image = form_image

# 	random_hex = secrets.token_hex(14)
# 	_, f_ext = os.path.splitext(image.filename)
# 	FileName = random_hex + f_ext
# 	modulePath = os.path.join('static/',module,str(id),'images')

# 	dirHandler(os.path.join(modulePath,"R"))
# 	FilePath = os.path.join(modulePath,"R",FileName)
# 	saving_path = os.path.join(os.getcwd(),FilePath)
# 	image.save(saving_path,optimize=True,quality=65)
# 	paths={
# 		"FilePathR":FilePath
# 	}

# 	resizing = changeImageSize(FilePath,modulePath,FileName)
# 	print(resizing)

# save_image(savedImage='IMG_5660.JPG',module="commerce/users",id=12)


#################################