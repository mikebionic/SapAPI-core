from main_pack import db_test, login_manager
from main_pack.config import Config
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main_pack.models_test.base.models import CreatedModifiedInfo, AddInf
from main_pack.base.dataMethods import apiDataFormat

# # !!! FIX: this is a hack for flask-login to login the user..
# # !!! should be updated to a single model for multi bindin' usage
# @login_manager.user_loader
# def load_user(UId):
# 	return Users.query.get(int(UId))


class Users(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_users"
	__bind_key__ = 'postgres_test'
	UId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	RpAccId = db_test.Column(db_test.Integer)
	UFullName = db_test.Column(db_test.String(100))
	UName = db_test.Column(db_test.String(60),nullable=False)
	UEmail = db_test.Column(db_test.String(100),unique=True)
	UPass = db_test.Column(db_test.String(60),nullable=False)
	UShortName = db_test.Column(db_test.String(10))
	EmpId = db_test.Column(db_test.Integer)
	UTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_user_type.UTypeId"))
	Wish = db_test.relationship('Wish',backref='users',lazy=True)
	Rating = db_test.relationship('Rating',backref='users',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='users',lazy=True)
	Image = db_test.relationship('Image',backref='users',lazy=True)
	
	def is_admin(self):
		return self.UTypeId == 1

	def get_id(self):
		return (self.UId)

	def get_reset_token(self,expires_sec=1800):
		s = Serializer(Config.SECRET_KEY,expires_sec)
		return s.dumps({"UId": self.UId}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(Config.SECRET_KEY)
		try:
			UId = s.loads(token)['UId']
		except Exception as ex:
			return None
		return	Users.query.get(UId)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		users = {
			"UId": self.UId,
			"CId": self.CId,
			"DivId": self.DivId,
			"RpAccId": self.RpAccId,
			"UFullName": self.UFullName,
			"UName": self.UName,
			"UEmail": self.UEmail,
			# "UPass": self.UPass,
			"UShortName": self.UShortName,
			"EmpId": self.EmpId,
			"UTypeId": self.UTypeId,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return users


class User_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_user_type"
	__bind_key__ = 'postgres_test'
	UTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	UTypeName_tkTM = db_test.Column(db_test.String(50))#,nullable=False)
	UTypeDesc_tkTM = db_test.Column(db_test.String(500))
	UTypeName_ruRU = db_test.Column(db_test.String(50))#,nullable=False)
	UTypeDesc_ruRU = db_test.Column(db_test.String(500))
	UTypeName_enUS = db_test.Column(db_test.String(50))#,nullable=False)
	UTypeDesc_enUS = db_test.Column(db_test.String(500))
	Users = db_test.relationship('Users',backref='user_type',lazy=True)

	def to_json_api(self):
		user_type = {
			"UTypeId": self.UTypeId,
			"UTypeName_tkTM": self.UTypeName_tkTM,
			"UTypeDesc_tkTM": self.UTypeDesc_tkTM,
			"UTypeName_ruRU": self.UTypeName_ruRU,
			"UTypeDesc_ruRU": self.UTypeDesc_ruRU,
			"UTypeName_enUS": self.UTypeName_enUS,
			"UTypeDesc_enUS": self.UTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return user_type


class Rp_acc(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_rp_acc"
	__bind_key__ = 'postgres_test'
	RpAccId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	UId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_users.UId"))
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	GenderId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_gender.GenderId"))
	NatId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_nationality.NatId"))
	RpAccStatusId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc_status.RpAccStatusId"))
	ReprId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_representative.ReprId"))
	RpAccTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc_type.RpAccTypeId"))
	WpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_work_period.WpId"))
	RpAccRegNo = db_test.Column(db_test.String(100),nullable=False,unique=True)
	RpAccUName = db_test.Column(db_test.String(60))
	RpAccUPass = db_test.Column(db_test.String(60))
	RpAccName = db_test.Column(db_test.String(255))
	RpAccAddress = db_test.Column(db_test.String(500))
	RpAccMobilePhoneNumber = db_test.Column(db_test.String(100))
	RpAccHomePhoneNumber = db_test.Column(db_test.String(100))
	RpAccWorkPhoneNumber = db_test.Column(db_test.String(100))
	RpAccWorkFaxNumber = db_test.Column(db_test.String(100))
	RpAccZipCode = db_test.Column(db_test.String(100))
	RpAccEMail = db_test.Column(db_test.String(100))
	RpAccFirstName = db_test.Column(db_test.String(100))
	RpAccLastName = db_test.Column(db_test.String(100))
	RpAccPatronomic = db_test.Column(db_test.String(100))
	RpAccBirthDate = db_test.Column(db_test.DateTime)
	RpAccResidency = db_test.Column(db_test.String(100))
	RpAccPassportNo = db_test.Column(db_test.String(100))
	RpAccPassportIssuePlace = db_test.Column(db_test.String(100))
	RpAccLangSkills = db_test.Column(db_test.String(100))
	RpAccSaleBalanceLimit = db_test.Column(db_test.Float,default=0)
	RpAccPurchBalanceLimit = db_test.Column(db_test.Float,default=0)
	Representative = db_test.relationship('Representative',backref='rp_acc',foreign_keys='Representative.RpAccId',lazy='dynamic')
	Accounting_info = db_test.relationship('Accounting_info',backref='rp_acc',lazy=True)
	Contact = db_test.relationship('Contact',backref='rp_acc',lazy=True)
	Image = db_test.relationship('Image',backref='rp_acc',lazy=True)
	Location = db_test.relationship('Location',backref='rp_acc',lazy=True)
	Resource = db_test.relationship('Resource',backref='last_vendor',lazy=True)
	Inv_line = db_test.relationship('Inv_line',backref='last_vendor',lazy=True)
	Order_inv_line = db_test.relationship('Order_inv_line',backref='last_vendor',lazy=True)
	Res_trans_inv_line = db_test.relationship('Res_trans_inv_line',backref='last_vendor',lazy=True)
	Rp_acc_price_list = db_test.relationship('Rp_acc_price_list',backref='rp_acc',lazy=True)
	Rp_acc_resource = db_test.relationship('Rp_acc_resource',backref='rp_acc',lazy=True)
	Rp_acc_trans_total = db_test.relationship('Rp_acc_trans_total',backref='rp_acc',lazy=True)
	Rp_acc_transaction = db_test.relationship('Rp_acc_transaction',backref='rp_acc',lazy=True)
	Sale_card = db_test.relationship('Sale_card',backref='rp_acc',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='rp_acc',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='rp_acc',lazy=True)
	Rating = db_test.relationship('Rating',backref='rp_acc',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_rp_acc = {
			"RpAccId": self.RpAccId,
			"CId": self.CId,
			"DivId": self.DivId,
			"EmpId": self.EmpId,
			"GenderId": self.GenderId,
			"NatId": self.NatId,
			"RpAccStatusId": self.RpAccStatusId,
			"ReprId": self.ReprId,
			"RpAccTypeId": self.RpAccTypeId,
			"WpId": self.WpId,			
			"RpAccRegNo": self.RpAccRegNo,
			"RpAccUName": self.RpAccUName,
			# "RpAccUPass": self.RpAccUPass,
			"RpAccName": self.RpAccName,
			"RpAccAddress": self.RpAccAddress,
			"RpAccMobilePhoneNumber": self.RpAccMobilePhoneNumber,
			"RpAccHomePhoneNumber": self.RpAccHomePhoneNumber,
			"RpAccWorkPhoneNumber": self.RpAccWorkPhoneNumber,
			"RpAccWorkFaxNumber": self.RpAccWorkFaxNumber,
			"RpAccZipCode": self.RpAccZipCode,
			"RpAccEMail": self.RpAccEMail,
			"RpAccFirstName": self.RpAccFirstName,
			"RpAccLastName": self.RpAccLastName,
			"RpAccPatronomic": self.RpAccPatronomic,
			"RpAccBirthDate": apiDataFormat(self.RpAccBirthDate),
			"RpAccResidency": self.RpAccResidency,
			"RpAccPassportNo": self.RpAccPassportNo,
			"RpAccPassportIssuePlace": self.RpAccPassportIssuePlace,
			"RpAccLangSkills": self.RpAccLangSkills,
			"RpAccSaleBalanceLimit": self.RpAccSaleBalanceLimit,
			"RpAccPurchBalanceLimit": self.RpAccPurchBalanceLimit,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc


class Rp_acc_status(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_rp_acc_status"
	__bind_key__ = 'postgres_test'
	RpAccStatusId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RpAccStatusName_tkTM = db_test.Column(db_test.String(100),nullable=False)
	RpAccStatusDesc_tkTM = db_test.Column(db_test.String(500))
	RpAccStatusName_ruRU = db_test.Column(db_test.String(100))
	RpAccStatusDesc_ruRU = db_test.Column(db_test.String(500))
	RpAccStatusName_enUS = db_test.Column(db_test.String(100))
	RpAccStatusdesc_enUS = db_test.Column(db_test.String(500))
	Rp_acc = db_test.relationship('Rp_acc',backref='rp_acc_status',lazy=True)

	def to_json_api(self):
		json_rp_acc_status = {
			"RpAccStatusId": self.RpAccStatusId,
			"RpAccStatusName_tkTM": self.RpAccStatusName_tkTM,
			"RpAccStatusDesc_tkTM": self.RpAccStatusDesc_tkTM,
			"RpAccStatusName_ruRU": self.RpAccStatusName_ruRU,
			"RpAccStatusDesc_ruRU": self.RpAccStatusDesc_ruRU,
			"RpAccStatusName_enUS": self.RpAccStatusName_enUS,
			"RpAccStatusdesc_enUS": self.RpAccStatusdesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc_status


class Rp_acc_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_rp_acc_type"
	__bind_key__ = 'postgres_test'
	RpAccTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RpAccTypeName_tkTM = db_test.Column(db_test.String(100),nullable=False)
	RpAccTypeDesc_tkTM = db_test.Column(db_test.String(500))
	RpAccTypeName_ruRU = db_test.Column(db_test.String(100))
	RpAccTypeDesc_ruRU = db_test.Column(db_test.String(500))
	RpAccTypeName_enUS = db_test.Column(db_test.String(100))
	RpAccTypeDesc_enUS = db_test.Column(db_test.String(500))
	Rp_acc = db_test.relationship('Rp_acc',backref='rp_acc_type',lazy=True)

	def to_json_api(self):
		json_rp_acc_type = {
			"RpAccTypeId": self.RpAccTypeId,
			"RpAccTypeName_tkTM": self.RpAccTypeName_tkTM,
			"RpAccTypeDesc_tkTM": self.RpAccTypeDesc_tkTM,
			"RpAccTypeName_ruRU": self.RpAccTypeName_ruRU,
			"RpAccTypeDesc_ruRU": self.RpAccTypeDesc_ruRU,
			"RpAccTypeName_enUS": self.RpAccTypeName_enUS,
			"RpAccTypeDesc_enUS": self.RpAccTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc_type