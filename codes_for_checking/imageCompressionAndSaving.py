
######### working example #####

import os
import sys
from PIL import Image
import secrets

def dirHandler(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except Exception as ex:
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
		dirHandler(os.path.join(modulePath,size))
		# makes the "module/id/R/blahblah.jpg"
		FilePath = os.path.join(modulePath,size,FileName)
				# join app root path with filepath of image
		# saving_path = os.path.join(current_app.root_path,FilePath)
		saving_path = os.path.join(os.getcwd(),FilePath)
		if not output_sizes[size]:
			image.save(saving_path,optimize=True,quality=65)
			paths["FilePath"+size]=FilePath
		else:
			image.thumbnail(output_sizes[size])
			image.save(saving_path)
			paths["FilePath"+size]=FilePath

	return paths


def save_image(form_image=None,savedImage=None,module="undefined",id="undefined"):
	if not form_image:
		image = Image.open(savedImage)
	if form_image:
		image = form_image

	random_hex = secrets.token_hex(14)
	_, f_ext = os.path.splitext(image.filename)
	FileName = random_hex + f_ext
	modulePath = os.path.join('static/',module,str(id),'images')

	resizing = changeImageSize(imageFile=image,modulePath=modulePath,FileName=FileName)
	print(resizing)

save_image(savedImage='IMG_5660.JPG',module="commerce/users",id=12)


################################


