
import uuid 
from datetime import datetime, timedelta

from main_pack.base import log_print
from main_pack.models import Register_request
from main_pack import db


def register_phone_number(phone_number):
	data = {}
	try:
		PhoneNumber = phone_number.strip()
		if len(PhoneNumber) < 10:
			log_print(f"{PhoneNumber} has length {len(PhoneNumber)}", "warning")
			raise Exception

		existing_register_request = Register_request.query\
			.filter_by(
				RegReqPhoneNumber = PhoneNumber,
				GCRecord = None)\
			.first()
		
		if existing_register_request:
			if existing_register_request.RegReqVerified:
				log_print(f"phone number exists: {str(existing_register_request)}", "warning")
				raise Exception
			
			else:
				existing_register_request.RegReqExpDate = datetime.now() + timedelta(minutes=10)
				db.session.commit()
				data = existing_register_request.to_json_api()
		
		else:
			new_register_request_data = {
				"RegReqGuid": uuid.uuid4(),
				"RegReqPhoneNumber": PhoneNumber,
				"RegReqVerified": 0,
				"RegReqExpDate": datetime.now() + timedelta(minutes=10)
			}
			new_register_request = Register_request(**new_register_request_data)
			db.session.add(new_register_request)
			db.session.commit()
			data = new_register_request.to_json_api()

	except Exception as ex:
		log_print(f"Register phone number exception: {ex}", 'warning')

	return data