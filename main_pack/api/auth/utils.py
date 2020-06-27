from flask import url_for
from main_pack import db,bcrypt,mail #,babel,gettext,lazy_gettext
from flask_mail import Message
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from main_pack.models.users.models import Users

from flask import jsonify,request
import jwt
from functools import wraps
from main_pack.config import Config

def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({'message':'Token is missing!'}), 401
		try:
			data=jwt.decode(token, Config.SECRET_KEY)
			current_user = Users.query.filter_by(UId=data['UId']).first()
		except:
			return jsonify({'message':'Token is invalid!'}), 401
		return f(current_user,*args,**kwargs)

	return decorated

def check_auth(username,password):
	user = Users.query.filter_by(UName=username).first()
	# if user and bcrypt.check_password_hash(user.UPass,password):
	if user and user.UPass==password:
		return True
	else:
		return False


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
	s = Serializer(current_app.config['SECRET_KEY'],1800)
	return s.dumps({'UName':UName,'UEmail':UEmail}).decode('utf-8')

def verify_register_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		UName = s.loads(token)['UName']
		UEmail = s.loads(token)['UEmail']
	except:
		return None
	return {'UName':UName,'UEmail':UEmail}

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