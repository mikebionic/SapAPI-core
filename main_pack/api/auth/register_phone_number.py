
from main_pack.models.Rp_acc import Rp_acc
from main_pack.base.cryptographyMethods import encodeJWT
import uuid
from datetime import datetime, timedelta

from main_pack.base import log_print
from main_pack.models import Register_request
from main_pack import db
from main_pack.config import Config


from main_pack.base import generate_random_code
from main_pack.api.common import configurePhoneNumber
from main_pack.api.common import send_data_to_sync_server


def login_phone_number(phone_number):
	data, message = {}, ""
	try:
		PhoneNumber = configurePhoneNumber(phone_number)
		if not PhoneNumber:
			message = "{}: {}".format("Invalid phone number", phone_number)
			log_print(message, "warning")
			raise Exception

		registered_phone_rp_acc = Rp_acc.query\
			.filter_by(
				RpAccMobilePhoneNumber = PhoneNumber,
				GCRecord = None
			).first()
		
		if not registered_phone_rp_acc:
			message = f"User not found!"
			log_print(f"{message}: {PhoneNumber}", "warning")
			raise Exception

		existing_register_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = PhoneNumber,
				GCRecord = None)\
			.first()

		if existing_register_request:
			if existing_register_request.RegReqVerified:
				existing_register_request.RegReqVerified = 0
				existing_register_request.RegReqExpDate = datetime.now() + timedelta(minutes=Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES)
				db.session.commit()
				data = existing_register_request.to_json_api()

		else:
			new_register_request_data = {
				"RegReqGuid": uuid.uuid4(),
				"RegReqPhoneNumber": PhoneNumber,
				"RegReqVerified": 0,
				"RegReqExpDate": datetime.now() + timedelta(minutes=Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES)
			}
			new_register_request = Register_request(**new_register_request_data)
			db.session.add(new_register_request)
			db.session.commit()
			data = new_register_request.to_json_api()

	except Exception as ex:
		log_print(f"Register phone number exception: {ex}", 'warning')

	return data, message


def register_phone_number(phone_number):
	data, message = {}, ""
	try:
		PhoneNumber = configurePhoneNumber(phone_number)
		if not PhoneNumber:
			message = "{}: {}".format("Invalid phone number", phone_number)
			log_print(message, "warning")
			raise Exception
		
		registered_phone_rp_acc = Rp_acc.query\
			.filter_by(
				RpAccMobilePhoneNumber = PhoneNumber,
				GCRecord = None
			).first()
		
		if registered_phone_rp_acc:
			message = f"Phone number {phone_number} is already taken"
			log_print(f"{message}: {PhoneNumber}", "warning")
			raise Exception

		existing_register_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = PhoneNumber,
				GCRecord = None)\
			.first()

		verify_code = generate_random_code()
		should_register = True
		if existing_register_request:
			existing_register_request.RegReqVerifyCode = verify_code
			existing_register_request.RegReqVerified = 0
			existing_register_request.RegReqExpDate = datetime.now() + timedelta(minutes=Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES)
			db.session.commit()
			data = existing_register_request.to_json_api()
			should_register = False

		elif not existing_register_request or should_register:
			new_register_request_data = {
				"RegReqGuid": uuid.uuid4(),
				"RegReqPhoneNumber": PhoneNumber,
				"RegReqVerifyCode": verify_code,
				"RegReqVerified": 0,
				"RegReqExpDate": datetime.now() + timedelta(minutes=Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES)
			}
			new_register_request = Register_request(**new_register_request_data)
			db.session.add(new_register_request)
			db.session.commit()
			data = new_register_request.to_json_api()

		if data:
			data["validator_phone_number"] = Config.REGISTER_REQUEST_VALIDATOR_PHONE_NUMBER
			data["RegReqVerifyCode"] = ""
			send_sms_register_api_request(PhoneNumber, verify_code)

	except Exception as ex:
		log_print(f"Register phone number exception: {ex}", 'warning')

	return data, message

def send_sms_register_api_request(phone_number, verify_code):
	send_data_to_sync_server(
		payload={
			"phone_number": phone_number,
			"verify_code": verify_code
		},
		url_path=Config.SMS_SYNCH_URL_PATH
	)
	return

def check_phone_number_register(phone_number):
	data, message = {}, ""
	try:
		PhoneNumber = configurePhoneNumber(phone_number)
		if not PhoneNumber:
			message = "{}: {}".format("Invalid phone number", phone_number)
			log_print(message, "warning")
			raise Exception

		registered_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = PhoneNumber,
				GCRecord = None)\
			.first()

		if not registered_request:
			message = "{}: {}".format("Phone number not present", phone_number)
			log_print(message, "warning")
			raise Exception
		
		if not registered_request.RegReqVerified: 
			message = "Phone number not validated yet"

		if registered_request.RegReqVerified:
			data = registered_request.to_json_api()
			encoded_token, _ = encodeJWT({"phone_number": PhoneNumber})
			data["token"] = encoded_token.decode('UTF-8')
			data["phone_number"] = PhoneNumber
			message = "Phone number verified"

	except Exception as ex:
		log_print(f"Check phone num register exception {ex}", "warning")

	return data, message


def verify_phone_number_register(phone_number, message_text = None):
	data, message = {}, ""
	try:
		PhoneNumber = configurePhoneNumber(phone_number)
		if not PhoneNumber:
			message = "{}: {}".format("Invalid phone number", phone_number)
			log_print(message, "warning")
			raise Exception

		registered_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = PhoneNumber,
				GCRecord = None)\
			.filter(
				datetime.now() < Register_request.RegReqExpDate,
				Register_request.RegReqVerified != 1)\
			.first()
		
		if not registered_request:
			message = f"{PhoneNumber} | {message_text} wasn't registered or expired"
			log_print(message, "warning")
			raise Exception
		
		registered_request.RegReqVerified = 1
		db.session.commit()
		data = registered_request.to_json_api()

	except Exception as ex:
		log_print(f"validate phone num register exception {ex}", "warning")

	return data, message