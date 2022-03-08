from flask_mail import Message

from main_pack import mail
from main_pack.config import Config

def send_email_message(emails = [], title = '', body = ''):
	msg = Message(
		title,
		body = body,
		sender = Config.MAIL_USERNAME,
		recipients = emails
	)
	print(msg)
	mail.send(msg)
	return