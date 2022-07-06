from flask import url_for, redirect, session
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
from functools import wraps
from flask_login import current_user

from main_pack.config import Config
from main_pack import mail, gettext


def ui_admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		if (not current_user or not "model_type" in session):
			try:
				return redirect(url_for('commerce_auth.login'))

			except:
				return redirect(url_for('commerce_auth.admin_login'))

		if (session["model_type"] != "user" or not current_user.is_admin()):
			# flash(lazy_gettext('You do not have access to that page!'), 'danger')
			return redirect(url_for('commerce.commerce'))

		return f(*args, **kwargs)

	return decorated


def send_reset_email(user, model_type="rp_acc"):
	url = 'commerce_auth.reset_token'
	token = user.get_reset_token()
	email = user.RpAccEMail if model_type == "rp_acc" else user.UEmail
	msg = Message(gettext('Password reset request'), sender=Config.MAIL_USERNAME, recipients=[email])
	msg.body = '''{}:
	{}
	{}. 
	'''.format(
		gettext('To reset your password, visit the following link'),
		url_for(url, token=token, _external=True),
		gettext('If you did not make this request then simply ignore this email')
	)
	mail.send(msg)


def get_register_token(username, email):
	s = Serializer(Config.SECRET_KEY,1800)
	return s.dumps({'username': username, 'email': email}).decode('utf-8')


def verify_register_token(token):
	s = Serializer(Config.SECRET_KEY)

	try:
		username = s.loads(token)['username']
		email = s.loads(token)['email']
	except Exception as ex:
		return None

	return {'username': username, 'email': email}


def send_register_email(username, email):
	token = get_register_token(username, email)
	msg = Message(gettext('Registration request'), sender=Config.MAIL_USERNAME, recipients=[email])
	msg_dear = gettext('Dear')
	msg_bodyText = gettext('You have requested the registration on ecommerce. Please follow the link to verify your email')
	msg_ending = gettext('If you did not make this request then simply ignore this email') 
	msg.body = f'''{msg_dear}, {username}
	{msg_bodyText}
	{url_for('commerce_auth.register_token', token=token, _external=True)}
	{msg_ending}
	'''
	mail.send(msg)