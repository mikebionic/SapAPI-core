from flask import request

from main_pack import db, lazy_gettext
from main_pack.api.auth import api
from main_pack.base.log_print import log_print

# -------------
from main_pack.api.auth.utils import token_required
from main_pack.api.response_handlers import handle_default_response


@api.post("/reset-password/")
@token_required
def reset_password(user):
	data, message, status_code = {}, "Password didn't update!", 400
	try:
		if user["model_type"] != "rp_acc":
			message = "This route is available only for Rp_acc"
			raise Exception(message)
		req = request.get_json()
		password = req.get('password')
		confirm_password = req.get('confirm_password')
		if not password or not confirm_password:
			message = f"Invalid or empty password field: {password} | {confirm_password}"
			raise Exception(message)
		
		if password != confirm_password:
			message = f"Passwords not same: {password} | {confirm_password}"
			raise Exception(message)
		
		current_user = user["current_user"]
		if user["model_type"] == "rp_acc":
			current_user.RpAccUPass = password
			db.session.commit()
			data, message, status_code = current_user.to_json_api(), "Password successfully updated!", 201
			data["RpAccUPass"] = password


	except Exception as e:
		log_print(f"Reset password api Excepion: {e}", "warning")

	return handle_default_response(data, message, status_code)