from main_pack import db, login_manager
from main_pack.config import Config
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
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
	UGuid = db.Column(UUID(as_uuid=True),unique=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResPriceGroupId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	RpAccId = db.Column(db.Integer)
	UFullName = db.Column(db.String(100))
	UName = db.Column(db.String(60),nullable=False)
	UEmail = db.Column(db.String(100),unique=True)
	UPass = db.Column(db.String(60),nullable=False)
	URegNo = db.Column(db.String(100),unique=True)
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
	
	# @property
	# def is_active(self):
	# 	return True

	# def is_authenticated(self):
	# 	return True

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
			"UGuid": self.UGuid,
			"CId": self.CId,
			"DivId": self.DivId,
			"RpAccId": self.RpAccId,
			"ResPriceGroupId": self.ResPriceGroupId,
			"UFullName": self.UFullName,
			"UName": self.UName,
			"UEmail": self.UEmail,
			# "UPass": self.UPass,
			"UShortName": self.UShortName,
			"URegNo": self.URegNo,
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
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
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
			"UTypeId": self.UTypeId,
			"UTypeName_tkTM": self.UTypeName_tkTM,
			"UTypeDesc_tkTM": self.UTypeDesc_tkTM,
			"UTypeName_ruRU": self.UTypeName_ruRU,
			"UTypeDesc_ruRU": self.UTypeDesc_ruRU,
			"UTypeName_enUS": self.UTypeName_enUS,
			"UTypeDesc_enUS": self.UTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return user_type


class Rp_acc(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc"
	RpAccId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpAccGuid = db.Column(UUID(as_uuid=True),unique=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UId = db.Column(db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	GenderId = db.Column(db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	NatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_nationality.NatId"))
	RpAccStatusId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc_status.RpAccStatusId"))
	ReprId = db.Column(db.Integer,db.ForeignKey("tbl_dk_representative.ReprId"))
	ResPriceGroupId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	RpAccTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc_type.RpAccTypeId"))
	WpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	RpAccRegNo = db.Column(db.String(100),nullable=False)
	RpAccUName = db.Column(db.String(60))
	RpAccUPass = db.Column(db.String(60))
	RpAccName = db.Column(db.String(255))
	RpAccAddress = db.Column(db.String(500))
	RpAccMobilePhoneNumber = db.Column(db.String(100))
	RpAccHomePhoneNumber = db.Column(db.String(100))
	RpAccWorkPhoneNumber = db.Column(db.String(100))
	RpAccWorkFaxNumber = db.Column(db.String(100))
	RpAccZipCode = db.Column(db.String(100))
	RpAccEMail = db.Column(db.String(100))
	RpAccFirstName = db.Column(db.String(100))
	RpAccLastName = db.Column(db.String(100))
	RpAccPatronomic = db.Column(db.String(100))
	RpAccBirthDate = db.Column(db.DateTime)
	RpAccResidency = db.Column(db.String(100))
	RpAccPassportNo = db.Column(db.String(100))
	RpAccPassportIssuePlace = db.Column(db.String(100))
	RpAccLangSkills = db.Column(db.String(100))
	RpAccSaleBalanceLimit = db.Column(db.Float,default=0)
	RpAccPurchBalanceLimit = db.Column(db.Float,default=0)
	RpAccLatitude = db.Column(db.Float,default=0.0)
	RpAccLongitude = db.Column(db.Float,default=0.0)
	Representative = db.relationship('Representative',backref='rp_acc',foreign_keys='Representative.RpAccId',lazy='dynamic')
	Accounting_info = db.relationship('Accounting_info',backref='rp_acc',lazy=True)
	Contact = db.relationship('Contact',backref='rp_acc',lazy=True)
	Image = db.relationship('Image',backref='rp_acc',lazy=True)
	Location = db.relationship('Location',backref='rp_acc',lazy=True)
	Resource = db.relationship('Resource',backref='last_vendor',lazy=True)
	Inv_line = db.relationship('Inv_line',backref='last_vendor',lazy=True)
	Order_inv_line = db.relationship('Order_inv_line',backref='last_vendor',lazy=True)
	Res_trans_inv_line = db.relationship('Res_trans_inv_line',backref='last_vendor',lazy=True)
	Rp_acc_price_list = db.relationship('Rp_acc_price_list',backref='rp_acc',lazy=True)
	Rp_acc_resource = db.relationship('Rp_acc_resource',backref='rp_acc',lazy=True)
	Rp_acc_trans_total = db.relationship('Rp_acc_trans_total',backref='rp_acc',lazy=True)
	Rp_acc_transaction = db.relationship('Rp_acc_transaction',backref='rp_acc',lazy=True)
	Sale_card = db.relationship('Sale_card',backref='rp_acc',lazy=True)
	Invoice = db.relationship('Invoice',backref='rp_acc',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='rp_acc',lazy=True)
	Rating = db.relationship('Rating',backref='rp_acc',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_rp_acc = {
			"RpAccId": self.RpAccId,
			"RpAccGuid": self.RpAccGuid,
			"CId": self.CId,
			"DivId": self.DivId,
			"EmpId": self.EmpId,
			"GenderId": self.GenderId,
			"NatId": self.NatId,
			"RpAccStatusId": self.RpAccStatusId,
			"ReprId": self.ReprId,
			"ResPriceGroupId": self.ResPriceGroupId,
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
			"RpAccLatitude": self.RpAccLatitude,
			"RpAccLongitude": self.RpAccLongitude,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc


class Rp_acc_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_status"
	RpAccStatusId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpAccStatusName_tkTM = db.Column(db.String(100),nullable=False)
	RpAccStatusDesc_tkTM = db.Column(db.String(500))
	RpAccStatusName_ruRU = db.Column(db.String(100))
	RpAccStatusDesc_ruRU = db.Column(db.String(500))
	RpAccStatusName_enUS = db.Column(db.String(100))
	RpAccStatusdesc_enUS = db.Column(db.String(500))
	Rp_acc = db.relationship('Rp_acc',backref='rp_acc_status',lazy=True)

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
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc_status


class Rp_acc_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_type"
	RpAccTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpAccTypeName_tkTM = db.Column(db.String(100),nullable=False)
	RpAccTypeDesc_tkTM = db.Column(db.String(500))
	RpAccTypeName_ruRU = db.Column(db.String(100))
	RpAccTypeDesc_ruRU = db.Column(db.String(500))
	RpAccTypeName_enUS = db.Column(db.String(100))
	RpAccTypeDesc_enUS = db.Column(db.String(500))
	Rp_acc = db.relationship('Rp_acc',backref='rp_acc_type',lazy=True)

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
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_rp_acc_type