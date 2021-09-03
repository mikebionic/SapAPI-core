import os
from datetime import datetime

from main_pack.models import Image
from main_pack.models import Sl_image


def run_clearer(path, model_type="image"):
	files_data = get_files_info_from_path(path)
	images_data = get_images_query_from_db(model_type)
	make_pop_merge_of_data(files_data, images_data)


def make_pop_merge_of_data(files_data, images_data):
	missing_in_list = list(filter(lambda d: d['filename'] not in images_data, files_data))
	for data in missing_in_list:
		os.remove(data["path"])


def get_files_info_from_path(path):
	# print("requested ", path)
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


def get_images_query_from_db(model_type = "image"):
	try:
		if model_type == "slider":
			image_query = Sl_image.query\
				.filter_by(GCRecord = None).all()
			data = [image.SlImgMainImgFileName for image in image_query]

		else:
			image_query = Image.query\
				.filter_by(GCRecord = None).all()

			data = [image.FileName for image in image_query]

	except Exception as ex:
		print(f"{datetime.now()} | image query exception: {ex}")

	return data