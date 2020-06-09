from flask import current_app
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

def changeImageSize(imageFile,modulePath,FileName):
	output_sizes = {
		"R":None,
		"M":(800,600),
		"S":(320,240),
	}
	paths={}
	for size in output_sizes:
		image = imageFile
		
		# create path according to a size abobe like "/images/M/blahblah.jpg"
		sizeSpecificFullPath = os.path.join(current_app.root_path,'static/',modulePath,size)
		# check that it exists or create one
		dirHandler(sizeSpecificFullPath)

		# makes the "module/id/R/blahblah.jpg" (required for db path info)
		FilePath = os.path.join(modulePath,size,FileName)

		# join the fullPath with filename to save to
		saving_path = os.path.join(sizeSpecificFullPath,FileName)
		if not output_sizes[size]:
			image.save(saving_path,optimize=True,quality=65)
			paths["FilePath"+size]=FilePath
		else:
			image.thumbnail(output_sizes[size])
			image.save(saving_path)
			paths["FilePath"+size]=FilePath

	return paths


def save_image(imageForm=None,savedImage=None,module="undefined",id="undefined"):
	random_hex = secrets.token_hex(14)
	modulePath = os.path.join(str(module),str(id),'images')
	
	if not imageForm:
		image = Image.open(savedImage)
		_, f_ext = os.path.splitext(image.filename)
		FileName = random_hex + f_ext

	if imageForm:
		# need to save the file to proceed compression and resizing if imageForm
		_, f_ext = os.path.splitext(imageForm.filename)
		FileName = random_hex + f_ext
		size = "R"

		sizeSpecificFullPath = os.path.join(current_app.root_path,'static/',modulePath,size)
		dirHandler(sizeSpecificFullPath)
		FilePath = os.path.join(modulePath,size,FileName)
		saving_path = os.path.join(sizeSpecificFullPath,FileName)
		imageForm.save(saving_path)
		print('it was a form now saved into:')
		print(saving_path)

		image = Image.open(imageForm)

	response = {
		"FileName":FileName
	}
	resizing = changeImageSize(imageFile=image,modulePath=modulePath,FileName=FileName)
	for image in resizing:
		response[image]=resizing[image]
	return response

# save_image(savedImage='IMG_5660.JPG',module="commerce/users",id=12)
