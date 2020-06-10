from main_pack import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main_pack.models.base.models import CreatedModifiedInfo, AddInf
from main_pack.base.dataMethods import apiDataFormat

@login_manager.user_loader
def load_user(UId):
	return Users.query.get(int(UId))

class Users(AddInf,CreatedModifiedInfo,db.Model,UserMixin):
	__tablename__="tbl_dk_users"
	UId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	RpAccId = db.Column(db.Integer)
	UFullName = db.Column(db.String(100))
	UName = db.Column(db.String(60),nullable=False)
	UEmail = db.Column(db.String(100),unique=True)
	UPass = db.Column(db.String(60),nullable=False)
	UShortName = db.Column(db.String(10))
	EmpId = db.Column(db.Integer)
	UTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_user_type.UTypeId"))
	Wish = db.relationship('Wish',backref='users',lazy=True)
	Rating = db.relationship('Rating',backref='users',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='users',lazy=True)
	Image = db.relationship('Image',backref='users',lazy=True)
	
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

	def to_json_api(self):
		users = {
			'UId':self.UId,
			'CId':self.CId,
			'DivId':self.DivId,
			'RpAccId':self.RpAccId,
			'UFullName':self.UFullName,
			'UName':self.UName,
			'UEmail':self.UEmail,
			'UPass':self.UPass,
			'UShortName':self.UShortName,
			'EmpId':self.EmpId,
			'UTypeId':self.UTypeId,
			'AddInf1':self.AddInf1,
			'AddInf2':self.AddInf2,
			'AddInf3':self.AddInf3,
			'AddInf4':self.AddInf4,
			'AddInf5':self.AddInf5,
			'AddInf6':self.AddInf6,
			'CreatedDate':apiDataFormat(self.CreatedDate),
			'ModifiedDate':apiDataFormat(self.ModifiedDate),
			'CreatedUId':self.CreatedUId,
			'ModifiedUId':self.ModifiedUId,
			'GCRecord':self.GCRecord
			}
		return users

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

	def to_json_api(self):
		user_type = {
			'UTypeId':self.UTypeId,
			'UTypeName_tkTM':self.UTypeName_tkTM,
			'UTypeDesc_tkTM':self.UTypeDesc_tkTM,
			'UTypeName_ruRU':self.UTypeName_ruRU,
			'UTypeDesc_ruRU':self.UTypeDesc_ruRU,
			'UTypeName_enUS':self.UTypeName_enUS,
			'UTypeDesc_enUS':self.UTypeDesc_enUS,
			'CreatedDate':apiDataFormat(self.CreatedDate),
			'ModifiedDate':apiDataFormat(self.ModifiedDate),
			'CreatedUId':self.CreatedUId,
			'ModifiedUId':self.ModifiedUId,
			'GCRecord':self.GCRecord
			}
		return user_type