from main_pack import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main_pack.models.base.models import CreatedModifiedInfo, AddInf

@login_manager.user_loader
def load_user(UId):
	return Users.query.get(int(UId))

class Users(AddInf,CreatedModifiedInfo,db.Model,UserMixin):
	__tablename__="tbl_dk_users"
	UId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UFullName = db.Column(db.String(100),nullable=False)
	UName = db.Column(db.String(60),nullable=False)
	UEmail = db.Column(db.String(100),unique=True,nullable =False)
	UPass = db.Column(db.String(60))
	UShortName = db.Column(db.String(10))
	EmpId = db.Column(db.Integer)
	UTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_user_type.UTypeId"))
	Wish = db.relationship('Wish',backref='users',lazy=True)
	Rating = db.relationship('Rating',backref='users',lazy=True)
	

	def is_admin(self):
		return self.UTypeId == 1

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

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)


class User_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_user_type"
	UTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	UTypeName_tkTM = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_tkTM = db.Column(db.String(500))
	UTypeName_ruRU = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_ruRU = db.Column(db.String(500))
	UTypeName_enUS = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_enUS = db.Column(db.String(500))
	Users = db.relationship('Users',backref='user_type',lazy=True)