from main_pack import bcrypt
from main_pack.config import Config
from main_pack.base import log_print

def configurePassword(password_req):
	password = None
	try:
		password_req = password_req.strip()
		if Config.HASHED_PASSWORDS == True:
			password = bcrypt.generate_password_hash(password_req).decode()
		else:
			password = password_req

	except Exception as ex:
		log_print(f"Password configure fail {ex}", "warning")

	return password


def checkPassword(password, password_request):
	state = False
	try:
		password = password.strip()
		password_request = password_request.strip()
		if Config.HASHED_PASSWORDS == True:
			state = bcrypt.check_password_hash(password, password_request)
		else:
			state = (password == password_request)

	except Exception as ex:
		log_print(f"Password check fail {ex}", "warning")

	return state