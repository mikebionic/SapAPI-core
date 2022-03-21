# -*- coding: utf-8 -*-
from main_pack.base import log_print
from main_pack import db
from .add_Rp_acc_dict import add_Rp_acc_dict


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

# if form.picture.data:
# 	imageFile = save_image(
# 		imageForm = form.picture.data,
# 		module = os.path.join("uploads","commerce","Rp_acc"),
# 		id = current_user.RpAccId)

# 	lastImage = Image.query.order_by(Image.ImgId.desc()).first()
# 	ImgId = lastImage.ImgId+1

# 	image = Image(
# 		ImgId = ImgId,
# 		ImgGuid = uuid.uuid4(),
# 		FileName = imageFile['FileName'],
# 		FilePath = imageFile['FilePath'],
# 		RpAccId = current_user.RpAccId)

# 	db.session.add(image)