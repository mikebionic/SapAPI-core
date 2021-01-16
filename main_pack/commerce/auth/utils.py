from flask import url_for,redirect
from main_pack.config import Config
from main_pack import db,bcrypt,mail,babel,gettext,lazy_gettext
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# auth and validation
from flask_login import current_user,login_required
# / auth and validation /

import os
from functools import wraps

def ui_admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		if not current_user:
			try:
				return redirect(url_for('commerce_auth.login'))

			except:
				return redirect(url_for('commerce_auth.admin_login'))
		
		elif not current_user.is_admin():
			# flash(lazy_gettext('You do not have access to that page!'), 'danger')
			return redirect(url_for('commerce.commerce'))

		return f(*args, **kwargs)

	return decorated


def send_reset_email(user):
	url = 'commerce_auth.reset_token'
	token = user.get_reset_token()
	msg = Message(gettext('Password reset request'), sender='noterply@demo.com',recipients=[user.UEmail])
	msg.body = f'''{gettext('To reset your password, visit the following link')}:
	{url_for(url,token=token,_external=True)}
	{gettext('If you did not make this request then simply ignore this email')}. 
	'''
	mail.send(msg)

def get_register_token(UName,UEmail):
	s = Serializer(Config.SECRET_KEY,1800)
	return s.dumps({'UName':UName,'UEmail':UEmail}).decode('utf-8')

def verify_register_token(token):
	s = Serializer(Config.SECRET_KEY)
	try:
		UName = s.loads(token)['UName']
		UEmail = s.loads(token)['UEmail']
	except Exception as ex:
		return None
	return {'UName':UName,'UEmail':UEmail}

def send_register_email(UName,UEmail):
	token = get_register_token(UName=UName,UEmail=UEmail)
	msg = Message(gettext('Registration request'),sender="noterply@mail.io",recipients=[UEmail])
	msg_dear = gettext('Dear')
	msg_bodyText = gettext('You have requested the registration on ecommerce. Please follow the link to verify your email')
	msg_ending = gettext('If you did not make this request then simply ignore this email') 
	msg.body = f'''{msg_dear}, {UName}
	{msg_bodyText}
	{url_for('commerce_auth.register_token',token=token,_external=True)}
	{msg_ending}
	'''
	mail.send(msg)