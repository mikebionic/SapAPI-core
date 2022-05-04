# -*- coding: utf-8 -*-
from flask import jsonify, request
from functools import wraps

from main_pack.config import Config
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
		auth_type = request.args.get("type","rp_acc",type=str)

		try:
			if not register_token:
				if "token" in request.headers:
					register_token = request.headers["token"]

			if not register_token:
				log_print("No token specified in header or query string parameter")
				raise Exception

			token_data = decodeJWT(register_token)

			if register_method == "email":
				# !!!TODO: Remove rp_acc validation from here
				email = token_data["email"].strip()

				if auth_type == "rp_acc":
					exiting_user = Rp_acc.query\
						.filter_by(
							RpAccEMail = email,
							GCRecord = None
						).first()
					if exiting_user:
						log_print("Email requested is already registered")
						raise Exception

					data = {
						"email": email
					}

			elif register_method == "phone_number":
				phone_number_data, _ = check_phone_number_register(token_data["phone_number"].strip())
				if not phone_number_data:
					log_print("Phone number not found in token_data or invalid")
					raise Exception

				if auth_type == "rp_acc":
					existing_user = Rp_acc.query\
						.filter_by(
							RpAccMobilePhoneNumber = phone_number_data["phone_number"],
							GCRecord = None,
						).first()
					if existing_user:
						log_print("Phone number requested is already registered")
						raise Exception

				data = {
					"phone_number": phone_number_data["phone_number"]
				}

		except Exception as ex:
			log_print(f"Register token required exception: {ex}")

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


def admin_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		auth_token = None
		current_user = None

		try:
			auth_token = get_bearer_from_header(request.headers.get('Authorization'))
			if not auth_token and 'x-access-token' in request.headers:
				auth_token = request.headers['x-access-token']

			if not auth_token:
				return jsonify({"message": "Token is missing!"}), 401

			if auth_token == Config.SYNCH_SHA:
				current_user = User.query.filter_by(UTypeId = 1).first()

			else:
				data = decodeJWT(auth_token)
				if "UId" in data:
					current_user = User.query\
						.filter_by(
							GCRecord = None,
							UTypeId = 1,
							UId = data['UId'])\
						.first()

		except Exception as ex:
			log_print(f"Admin required exception {ex}")

		if not current_user:
			return jsonify({"message": "Token is invalid!"}), 401

		user = {
			"model_type": 'user',
			"current_user": current_user
		}

		return f(user, *args,**kwargs)

	return decorated


def checkout_auth_handler(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		auth_token = None
		current_user = None
		model_type = "rp_acc"

		try:
			auth_token = get_bearer_from_header(request.headers.get('Authorization'))
			if not auth_token and 'x-access-token' in request.headers:
				auth_token = request.headers['x-access-token']

			if auth_token:
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

			if not auth_token:
				if Config.USE_APP_WITHOUT_AUTH:
					current_user = Rp_acc.query\
						.filter_by(
							RpAccGuid = Config.WITHOUT_AUTH_CHECKOUT_RPACCGUID,
							GCRecord = None)\
						.first()
					model_type = "rp_acc"

				if not current_user:
					return jsonify({"message": "Failed to checkout with anonymous user!"}), 401

			user = {
				"model_type": model_type,
				"current_user": current_user
			}

		except Exception as ex:
			log_print(f"Checkout auth handler exception {ex}")

		if not current_user:
			return jsonify({"message": "Token is invalid!"}), 401

		return f(user, *args,**kwargs)

	return decorated