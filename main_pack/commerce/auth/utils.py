from main_pack import db, bcrypt, mail
from flask_mail import Message
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password reset request', sender='noterply@demo.com',recipients=[user.EMail])
	msg.body = f'''To reset your password, visit the following link:
	{url_for('auth.reset_token',token=token,_external=True)}
	If you did not make this request then simply ignore this email. 
	'''
	mail.send(msg)

def get_register_token(UName,EMail):
	s = Serializer(current_app.config['SECRET_KEY'],1800)
	return s.dumps({'UName':UName,'EMail':EMail}).decode('utf-8')

def verify_register_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		UName = s.loads(token)['UName']
		EMail = s.loads(token)['EMail']
	except:
		return None
	return {'UName':UName,'EMail':EMail}

def send_register_email(UName,EMail):
	token = get_register_token(UName=UName,EMail=EMail)
	msg = Message('Password reset request', sender='noterply@demo.com',recipients=[EMail])
	msg.body = f'''Dear, {UName}
	You have requested the registration on ecommerce.
	Please follow the link to verify your email!
	{url_for('auth.register_token',token=token,_external=True)}
	If you did not make this request then simply ignore this email. 
	'''
	mail.send(msg)