import os
from datetime import datetime

from main_pack.models import Image

def run_clearer(path):

	files_data = get_files_info_from_path(path)
	images_data = get_images_query_from_db()
	print("daaaaaa     ", files_data)

	print("data    ", images_data)

	make_pop_merge_of_data(files_data, images_data)

def make_pop_merge_of_data(files_data, images_data):

	print(len(files_data))

	for data in files_data:
		if data["filename"] in images_data:
			images_data.pop(images_data.index(data["filename"]))
		
			files_data.pop(files_data.index(data))
			print("------------")
	
	print(len(files_data))



def get_files_info_from_path(path):
	print("requested ", path)
	data = []
	filesonly = []

	try:
		for path, subdirs, files in os.walk(path):
			for name in files:
				data.append({
					"filename": name,
					"path": os.path.join(path, name)
				})
				filesonly.append(name)

	except Exception as ex:
		print(f"{datetime.now()} | getting files from path exceptions: {ex}")

	return data

def get_images_query_from_db():

	try:
		image_query = Image.query\
			.filter_by(GCRecord = None).all()
		
		data = [image.FileName for image in image_query]

	except Exception as ex:
		print(f"{datetime.now()} | image query exception: {ex}")

	return data