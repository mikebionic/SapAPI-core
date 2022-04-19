# -*- coding: utf-8 -*-
import os
import uuid
from main_pack import db
from main_pack.base import log_print
from .add_Rp_acc_dict import add_Rp_acc_dict
from main_pack.models import Image
from main_pack.api.commerce.image_api import remove_image
from main_pack.base.imageMethods import save_image


def update_rp_acc_profile(req, model_type, current_user, session = None):
	data = {}
	try:
		rp_acc_info = add_Rp_acc_dict(req)
		rpAccData = {
			"RpAccUName": rp_acc_info["RpAccUName"],
			"RpAccName": rp_acc_info["RpAccName"],
			"RpAccAddress": rp_acc_info["RpAccAddress"],
			"RpAccHomePhoneNumber": rp_acc_info["RpAccHomePhoneNumber"],
			"RpAccZipCode": rp_acc_info["RpAccZipCode"],
			"RpAccWorkPhoneNumber": rp_acc_info["RpAccWorkPhoneNumber"],
			"RpAccWorkFaxNumber": rp_acc_info["RpAccWorkFaxNumber"],
			"RpAccWebAddress": rp_acc_info["RpAccWebAddress"],
		}
		current_user.update(**rpAccData)
		db.session.commit()
		data = current_user.to_json_api()

	except Exception as ex:
		log_print(f"v1 Rp_acc update Exception: {ex}")

	return data


def update_profile_picture(file, model_type, current_user, session = None, removeOthers = 0):
	data, message = {}, "Error updating picture"
	try:
		userId = current_user.RpAccId if model_type == "rp_acc" else current_user.UId
		imageFile = save_image(
			imageForm = file,
			module = os.path.join("uploads","commerce","Rp_acc" if model_type == "rp_acc" else "User"),
			id = userId)

		lastImage = Image.query.with_entities(Image.ImgId).order_by(Image.ImgId.desc()).first()
		ImgId = lastImage.ImgId + 1
		this_image_data = {
			"ImgId": ImgId,
			"ImgGuid": uuid.uuid4(),
			"FileName": imageFile['FileName'],
			"FilePath": imageFile['FilePath'],
		}
		if model_type == "rp_acc":
			this_image_data["RpAccId"] = current_user.RpAccId
		else:
			this_image_data["UId"] = current_user.UId
		
		this_image = Image(**this_image_data)
		db.session.add(this_image)
		db.session.commit()
		data, message = this_image.to_json_api(), "Picture successfully updated!"

		if removeOthers:
			try:
				filters = {}
				if not current_user or not model_type:
					log_print("no current_user or model_type")
					raise Exception

				if model_type == "rp_acc":
					filters["RpAccId"] = current_user.RpAccId
					if not filters["RpAccId"]:
						raise Exception

				else:
					filters["UId"] = current_user.UId
					if not filters["RpAccId"]:
						raise Exception

				other_images = Image.query\
					.filter_by(**filters)\
					.filter(Image.ImgId != this_image.ImgId).all()

				for other_image in other_images:
					remove_image("image",other_image.FileName)
					db.session.delete(other_image)

				db.session.commit()

			except Exception as ex:
				log_print(f"profile image removing exception {ex}")

	except Exception as ex:
		log_print(f"Update profile picture api error: {ex}")
	return data, message