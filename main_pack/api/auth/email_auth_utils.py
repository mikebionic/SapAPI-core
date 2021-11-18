from flask_mail import Message
import uuid
from datetime import datetime, timedelta

from main_pack import db
from main_pack import mail, gettext
from main_pack.base import log_print
from main_pack.config import Config

from main_pack.base import generate_random_code
from main_pack.api.common import configureEmail

from main_pack.models.Rp_acc import Rp_acc
from main_pack.models import Register_request


def register_email(requested_email):
	data, message = {}, ""
	try:
		email = configureEmail(requested_email)
		if not email:
			message = "{}: {}".format("Invalid email", requested_email)
			log_print(message, "warning")
			raise Exception
		
		registered_rp_acc = Rp_acc.query\
			.filter_by(
				RpAccEMail = email,
				GCRecord = None
			).first()

		if registered_rp_acc:
			message = f"Email is already taken"
			log_print(f"{message}: {email}", "warning")
			raise Exception

		existing_register_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = email,
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
				"RegReqPhoneNumber": email,
				"RegReqVerifyCode": verify_code,
				"RegReqVerified": 0,
				"RegReqExpDate": datetime.now() + timedelta(minutes=Config.REGISTER_REQUEST_EXPIRE_TIME_MINUTES)
			}
			new_register_request = Register_request(**new_register_request_data)
			db.session.add(new_register_request)
			db.session.commit()
			data = new_register_request.to_json_api()

		if data:
			data["RegReqVerifyCode"] = ""
			send_register_email(email, verify_code)

	except Exception as ex:
		log_print(f"Register email exception: {ex}", 'warning')

	return data, message


def send_register_email(email, verify_code):
	msg = Message(gettext('Registration request'), sender=Config.MAIL_USERNAME, recipients=[email])
	msg_bodyText = gettext('You have requested the registration on ecommerce. Please follow the link to verify your email')
	msg_ending = gettext('If you did not make this request then simply ignore this email') 
	msg.body = f'''
	{msg_bodyText}
	{verify_code}
	{msg_ending}
	'''
	mail.send(msg)