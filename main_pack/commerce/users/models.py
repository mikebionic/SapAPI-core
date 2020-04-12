from main_pack import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(UId):
	return Users.query.get(int(UId))

class Users(db.Model,UserMixin):
	__tablename__="tbl_me_users"
	UId = db.Column(db.Integer,nullable=False,primary_key=True)
	EMail = db.Column(db.String(120), unique=True, nullable =False)
	UFullName = db.Column(db.String(100))
	UName = db.Column(db.String(50),nullable=False)
	UPass = db.Column(db.String(60),nullable=False)
	UType = db.Column(db.Integer)
	def get_id(self):
		return (self.UId)

	def get_reset_token(self,expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'UId':self.UId}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			UId = s.loads(token)['UId']
		except:
			return None
		return	Users.query.get(UId)
	def __repr__ (self):
		return "Users('{}','{}')".format(self.UId,self.UName)