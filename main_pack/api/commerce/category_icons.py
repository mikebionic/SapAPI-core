import os
from datetime import datetime
from flask import (
	url_for,
	make_response,
	jsonify,
)

from main_pack.base.imageMethods import allowed_icon
from main_pack.config import Config
from . import api

@api.route("/category_icons/")
def category_icons():
	data = []
	icons_path = os.path.join("commerce","icons","categories")
	full_icons_path = os.path.join(Config.STATIC_FOLDER_LOCATION,icons_path)
	folders = os.listdir(full_icons_path)

	for folder in folders:
		try:
			folder_icons = os.listdir(os.path.join(full_icons_path,folder))
			icons = []
			for icon in folder_icons:
				if allowed_icon(icon):
					iconInfo = {
						"url": url_for('commerce_api.get_icon',category=folder,file_name=icon),
						"icon_name": icon,
						"category": folder
					}
					icons.append(iconInfo)

			data.append({folder: icons})
		except Exception as ex:
			print(f"{datetime.now()} | API category_icons Exception: {ex}")

	res = {
		"status": 1 if len(data) > 0 else 0,
		"message": "All icons",
		"data": data,
		"total": len(data)
	}
	response = make_response(jsonify(res), 200)
	return response
	