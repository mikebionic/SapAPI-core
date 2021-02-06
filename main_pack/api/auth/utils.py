# -*- coding: utf-8 -*-
from flask import url_for, jsonify, request
import jwt
from functools import wraps
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from main_pack.config import Config
from main_pack import db, bcrypt, mail
from main_pack.models.users.models import Users, Rp_acc, Device
from main_pack.activation.customer.utils import check_device_activation


def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({"message": "Token is missing!"}), 401

		try:
			data = jwt.decode(token, Config.SECRET_KEY)

			if "UId" in data:
				model_type = 'user'
				current_user = Users.query\
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
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({"message": "Token is missing!"}), 401
		
		if token != Config.SYNCH_SHA:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(*args,**kwargs)

	return decorated


def check_auth(auth_type, user_model, password):
	auth_status = False

	if (auth_type == "user"):

		if Config.HASHED_PASSWORDS == True:
			auth_status = bcrypt.check_password_hash(user_model.UPass, password)
		else:
			auth_status = (user_model.UPass == password)

	elif (auth_type == "rp_acc"):

		if Config.HASHED_PASSWORDS == True:
			auth_status = bcrypt.check_password_hash(user_model.RpAccUPass, password)
		else:
			auth_status = (user_model.RpAccUPass == password)

	elif (auth_type == "device"):
		if check_device_activation(device_model = user_model):
			auth_status = True

	return auth_status


# Email validation functions
def send_reset_email(user):
	url = 'commerce_auth.reset_token'
	token = user.get_reset_token()
	msg = Message(lazy_gettext('Password reset request'), sender='noterply@demo.com',recipients=[user.UEmail])
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
	msg = Message(lazy_gettext('Password reset request'), sender='noterply@demo.com',recipients=[UEmail])
	msg.body = f'''{lazy_gettext('Dear')}, {UName}
	{lazy_gettext('You have requested the registration on ecommerce')}.
	{lazy_gettext('Please follow the link to verify your email')}!
	{url_for('commerce_auth.register_token',token=token,_external=True)}
	{lazy_gettext('If you did not make this request then simply ignore this email')}. 
	'''
	mail.send(msg)