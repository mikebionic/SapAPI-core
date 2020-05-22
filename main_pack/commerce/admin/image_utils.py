import os, secrets
from flask import current_app
from PIL import Image

def save_picture(form_picture,path,imgType):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path,'static/commerce/images/'+path,picture_fn)
	form_picture.save(picture_path)
	if imgType=='logo':
		output_size = (125,125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
	if imgType=='resource':
		output_size = (600,600)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
	return picture_fn