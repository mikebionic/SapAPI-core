# -*- coding: utf-8 -*-
from flask import url_for, jsonify, request
from functools import wraps
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from main_pack import lazy_gettext
from main_pack.config import Config
from main_pack import mail
from main_pack.models import User, Rp_acc, Device

from main_pack.api.auth.register_phone_number import check_phone_number_register
from main_pack.base import log_print
from main_pack.base.cryptographyMethods import decodeJWT


def get_bearer_from_header(auth_header):
	auth_token = None

	try:
		auth_header.split(" ")[0].lower().index("bearer")
		auth_token = auth_header.split(" ")[1]
	except:
		pass
		# log_print("Token malformed, couldn't get bearer token")

	return auth_token

def register_token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		data = {}

		register_method = request.args.get("method","email",type=str)
		register_token = request.args.get("token","",type=str)
		auth_type = request.args.get("type","user",type=str)

		print("checking decorator ", register_method, register_token, auth_type)

		try:
			if not register_token:
				if "token" in request.headers:
					register_token = request.headers["token"]

			if not register_token:
				raise Exception

			token_data = decodeJWT(register_token)

			if register_method == "email":
				username = token_data["username"].strip()
				email = token_data["email"].strip()
			
				if auth_type == "rp_acc":
					exiting_user = Rp_acc.query\
						.filter_by(
							RpAccUName = username, 
							RpAccUEmail = email,
							GCRecord = None
						).first()
					if exiting_user:
						log_print("Email or Username requested is already registered")
						raise Exception
					
					data = {
						"username": username,
						"email": email
					}
			
			elif register_method == "phone-number":
				phone_number, _ = check_phone_number_register(token_data["phone_number"].strip())
				if not phone_number:
					raise Exception
				
				if auth_type == "rp_acc":
					existing_user = Rp_acc.query\
						.filter_by(
							RpAccMobilePhoneNumber = phone_number,
							GCRecord = None,
						).first()
					if existing_user:
						log_print("Phone number requested is already registered")
						raise Exception
				
				data = {
					"phone_number": phone_number
				}

		except:
			pass

		return f(data,*args,**kwargs)

	return decorated


def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		auth_token = None

		auth_token = get_bearer_from_header(request.headers.get('Authorization'))

		if not auth_token and 'x-access-token' in request.headers:
			auth_token = request.headers['x-access-token']

		if not auth_token:
			return jsonify({"message": "Token is missing!"}), 401

		try:
			data = decodeJWT(auth_token)

			if "UId" in data:
				model_type = 'user'
				current_user = User.query\
					.filter_by(GCRecord = None, UId = data['UId'])\
					.first()

			elif "RpAccId" in data:
				model_type = 'rp_acc'
				current_user = Rp_acc.query\
					.filter_by(GCRecord = None, RpAccId = data['RpAccId'])\
					.first()

			elif "DevId" in data:
				model_type = 'device'
				current_user = Device.query\
					.filter_by(GCRecord = None, DevId = data['DevId'])\
					.first()

			user = {
				"model_type": model_type,
				"current_user": current_user
			}

		except Exception as ex:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(user,*args,**kwargs)

	return decorated


def sha_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		auth_token = None

		auth_token = get_bearer_from_header(request.headers.get('Authorization'))
		if not auth_token and 'x-access-token' in request.headers:
			auth_token = request.headers['x-access-token']

		if not auth_token:
			return jsonify({"message": "Token is missing!"}), 401

		if auth_token != Config.SYNCH_SHA:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(*args,**kwargs)

	return decorated


# Email validation functions
def send_reset_email(user):
	url = 'commerce_auth.reset_token'
	token = user.get_reset_token()
	msg = Message(lazy_gettext('Password reset request'), sender=Config.MAIL_USERNAME,recipients=[user.UEmail])
	msg.body = f'''{lazy_gettext('To reset your password, visit the following link')}:
	{url_for(url,token=token,_external=True)}
	{lazy_gettext('If you did not make this request then simply ignore this email')}.
	'''
	mail.send(msg)

def get_register_token(UName,UEmail):
	s = Serializer(Config.SECRET_KEY,1800)
	return s.dumps({"UName": UName, "UEmail": UEmail}).decode('utf-8')

def verify_register_token(token):
	s = Serializer(Config.SECRET_KEY)
	try:
		UName = s.loads(token)['UName']
		UEmail = s.loads(token)['UEmail']
	except Exception as ex:
		return None
	return {"UName": UName, "UEmail": UEmail}

def send_register_email(UName,UEmail):
	token = get_register_token(UName=UName,UEmail=UEmail)
	msg = Message(lazy_gettext('Password reset request'), sender=Config.MAIL_USERNAME,recipients=[UEmail])
	msg.body = f'''{lazy_gettext('Dear')}, {UName}
	{lazy_gettext('You have requested the registration on ecommerce')}.
	{lazy_gettext('Please follow the link to verify your email')}!
	{url_for('commerce_auth.register_token',token=token,_external=True)}
	{lazy_gettext('If you did not make this request then simply ignore this email')}.
	'''
	mail.send(msg)