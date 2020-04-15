from flask import url_for
from main_pack import db, bcrypt, mail
from flask_mail import Message
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def send_reset_email(user):
	url = 'auth.reset_token_commerce'
	token = user.get_reset_token()
	msg = Message('Password reset request', sender='noterply@demo.com',recipients=[user.UEmail])
	msg.body = f'''To reset your password, visit the following link:
	{url_for(url,token=token,_external=True)}
	If you did not make this request then simply ignore this email. 
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
	msg = Message('Password reset request', sender='noterply@demo.com',recipients=[UEmail])
	msg.body = f'''Dear, {UName}
	You have requested the registration on ecommerce.
	Please follow the link to verify your email!
	{url_for('auth.register_token_commerce',token=token,_external=True)}
	If you did not make this request then simply ignore this email. 
	'''
	mail.send(msg)