from flask import session
from main_pack import db, login_manager
from main_pack.config import Config
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main_pack.models.base.models import CreatedModifiedInfo, AddInf
from main_pack.base.dataMethods import apiDataFormat


@login_manager.user_loader
def load_user(id):
	if (not "user_type" in session):
		return None

	if (session["user_type"] == "user"):
		return Users.query.get(int(id))

	elif (session["user_type"] == "rp_acc"):
		return Rp_acc.query.get(int(id))

	return None


class Users(AddInf,CreatedModifiedInfo,db.Model,UserMixin):
	__tablename__="tbl_dk_users"
	UId = db.Column("UId",db.Integer,nullable=False,primary_key=True)
	UGuid = db.Column("UGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	RpAccId = db.Column("RpAccId",db.Integer)
	UFullName = db.Column("UFullName",db.String(100))
	UName = db.Column("UName",db.String(60),nullable=False)
	UEmail = db.Column("UEmail",db.String(100),unique=True)
	UPass = db.Column("UPass",db.String(60),nullable=False)
	URegNo = db.Column("URegNo",db.String(100),unique=True)
	UShortName = db.Column("UShortName",db.String(10))
	EmpId = db.Column("EmpId",db.Integer)
	UTypeId = db.Column("UTypeId",db.Integer,db.ForeignKey("tbl_dk_user_type.UTypeId"))
	ULastActivityDate = db.Column("ULastActivityDate",db.DateTime,default=datetime.now())
	ULastActivityDevice = db.Column("ULastActivityDevice",db.String(100))
	Wish = db.relationship("Wish",backref='users',lazy=True)
	Rating = db.relationship("Rating",backref='users',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='users',lazy=True)
	Image = db.relationship("Image",backref='users',lazy=True)
	
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
		json_data = {
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
			"ULastActivityDate": apiDataFormat(self.ULastActivityDate),
			"ULastActivityDevice": self.ULastActivityDevice,
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
		return json_data


class User_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_user_type"
	UTypeId = db.Column("UTypeId",db.Integer,nullable=False,primary_key=True)
	UTypeName_tkTM = db.Column("UTypeName_tkTM",db.String(50))#,nullable=False)
	UTypeDesc_tkTM = db.Column("UTypeDesc_tkTM",db.String(500))
	UTypeName_ruRU = db.Column("UTypeName_ruRU",db.String(50))#,nullable=False)
	UTypeDesc_ruRU = db.Column("UTypeDesc_ruRU",db.String(500))
	UTypeName_enUS = db.Column("UTypeName_enUS",db.String(50))#,nullable=False)
	UTypeDesc_enUS = db.Column("UTypeDesc_enUS",db.String(500))
	Users = db.relationship("Users",backref='user_type',lazy=True)

	def to_json_api(self):
		json_data = {
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
		return json_data


class Rp_acc(AddInf,CreatedModifiedInfo,db.Model,UserMixin):
	__tablename__="tbl_dk_rp_acc"
	RpAccId = db.Column("RpAccId",db.Integer,nullable=False,primary_key=True)
	RpAccGuid = db.Column("RpAccGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	NatId = db.Column("NatId",db.Integer,db.ForeignKey("tbl_dk_nationality.NatId"))
	RpAccStatusId = db.Column("RpAccStatusId",db.Integer,db.ForeignKey("tbl_dk_rp_acc_status.RpAccStatusId"))
	ReprId = db.Column("ReprId",db.Integer,db.ForeignKey("tbl_dk_representative.ReprId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	RpAccTypeId = db.Column("RpAccTypeId",db.Integer,db.ForeignKey("tbl_dk_rp_acc_type.RpAccTypeId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	RpAccRegNo = db.Column("RpAccRegNo",db.String(100),nullable=False)
	RpAccUName = db.Column("RpAccUName",db.String(60))
	RpAccUPass = db.Column("RpAccUPass",db.String(60))
	RpAccName = db.Column("RpAccName",db.String(255))
	DbGuid = db.Column("DbGuid",UUID(as_uuid=True))
	DeviceQty = db.Column("DeviceQty",db.Integer)
	UnusedDeviceQty = db.Column("UnusedDeviceQty",db.Integer)
	RpAccAddress = db.Column("RpAccAddress",db.String(500))
	RpAccMobilePhoneNumber = db.Column("RpAccMobilePhoneNumber",db.String(100))
	RpAccHomePhoneNumber = db.Column("RpAccHomePhoneNumber",db.String(100))
	RpAccWorkPhoneNumber = db.Column("RpAccWorkPhoneNumber",db.String(100))
	RpAccWorkFaxNumber = db.Column("RpAccWorkFaxNumber",db.String(100))
	RpAccZipCode = db.Column("RpAccZipCode",db.String(100))
	RpAccEMail = db.Column("RpAccEMail",db.String(100))
	RpAccFirstName = db.Column("RpAccFirstName",db.String(100))
	RpAccLastName = db.Column("RpAccLastName",db.String(100))
	RpAccPatronomic = db.Column("RpAccPatronomic",db.String(100))
	RpAccBirthDate = db.Column("RpAccBirthDate",db.DateTime)
	RpAccResidency = db.Column("RpAccResidency",db.String(100))
	RpAccPassportNo = db.Column("RpAccPassportNo",db.String(100))
	RpAccPassportIssuePlace = db.Column("RpAccPassportIssuePlace",db.String(100))
	RpAccLangSkills = db.Column("RpAccLangSkills",db.String(100))
	RpAccSaleBalanceLimit = db.Column("RpAccSaleBalanceLimit",db.Float,default=0)
	RpAccPurchBalanceLimit = db.Column("RpAccPurchBalanceLimit",db.Float,default=0)
	RpAccLastActivityDate = db.Column("RpAccLastActivityDate",db.DateTime,default=datetime.now())
	RpAccLastActivityDevice = db.Column("RpAccLastActivityDevice",db.String(100))
	RpAccLatitude = db.Column("RpAccLatitude",db.Float,default=0.0)
	RpAccLongitude = db.Column("RpAccLongitude",db.Float,default=0.0)
	Representative = db.relationship("Representative",backref='rp_acc',foreign_keys='Representative.RpAccId',lazy=True)
	Accounting_info = db.relationship("Accounting_info",backref='rp_acc',lazy=True)
	Contact = db.relationship("Contact",backref='rp_acc',lazy=True)
	Image = db.relationship("Image",backref='rp_acc',lazy=True)
	Location = db.relationship("Location",backref='rp_acc',lazy=True)
	Resource = db.relationship("Resource",backref='last_vendor',lazy=True)
	Inv_line = db.relationship("Inv_line",backref='last_vendor',lazy=True)
	Order_inv_line = db.relationship("Order_inv_line",backref='last_vendor',lazy=True)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='last_vendor',lazy=True)
	Rp_acc_price_list = db.relationship("Rp_acc_price_list",backref='rp_acc',lazy=True)
	Rp_acc_resource = db.relationship("Rp_acc_resource",backref='rp_acc',lazy=True)
	Rp_acc_trans_total = db.relationship("Rp_acc_trans_total",backref='rp_acc',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='rp_acc',lazy=True)
	Sale_card = db.relationship("Sale_card",backref='rp_acc',lazy=True)
	Invoice = db.relationship("Invoice",backref='rp_acc',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='rp_acc',lazy=True)
	Rating = db.relationship("Rating",backref='rp_acc',lazy=True)
	Device = db.relationship("Device",backref='rp_acc',lazy=True)

	def get_reset_token(self,expires_sec=1800):
		s = Serializer(Config.SECRET_KEY,expires_sec)
		return s.dumps({"RpAccId": self.RpAccId}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(Config.SECRET_KEY)
		try:
			RpAccId = s.loads(token)['RpAccId']
		except Exception as ex:
			return None
		return	Rp_acc.query.get(RpAccId)

	def get_id(self):
		return (self.RpAccId)
	
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
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
			"DbGuid": self.DbGuid,
			"DeviceQty": self.DeviceQty,
			"UnusedDeviceQty": self.UnusedDeviceQty,
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
			"RpAccLastActivityDate": apiDataFormat(self.RpAccLastActivityDate),
			"RpAccLastActivityDevice": self.RpAccLastActivityDevice,
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
		return json_data


class Rp_acc_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_status"
	RpAccStatusId = db.Column("RpAccStatusId",db.Integer,nullable=False,primary_key=True)
	RpAccStatusName_tkTM = db.Column("RpAccStatusName_tkTM",db.String(100),nullable=False)
	RpAccStatusDesc_tkTM = db.Column("RpAccStatusDesc_tkTM",db.String(500))
	RpAccStatusName_ruRU = db.Column("RpAccStatusName_ruRU",db.String(100))
	RpAccStatusDesc_ruRU = db.Column("RpAccStatusDesc_ruRU",db.String(500))
	RpAccStatusName_enUS = db.Column("RpAccStatusName_enUS",db.String(100))
	RpAccStatusdesc_enUS = db.Column("RpAccStatusdesc_enUS",db.String(500))
	Rp_acc = db.relationship("Rp_acc",backref='rp_acc_status',lazy=True)

	def to_json_api(self):
		json_data = {
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
		return json_data


class Rp_acc_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_type"
	RpAccTypeId = db.Column("RpAccTypeId",db.Integer,nullable=False,primary_key=True)
	RpAccTypeName_tkTM = db.Column("RpAccTypeName_tkTM",db.String(100),nullable=False)
	RpAccTypeDesc_tkTM = db.Column("RpAccTypeDesc_tkTM",db.String(500))
	RpAccTypeName_ruRU = db.Column("RpAccTypeName_ruRU",db.String(100))
	RpAccTypeDesc_ruRU = db.Column("RpAccTypeDesc_ruRU",db.String(500))
	RpAccTypeName_enUS = db.Column("RpAccTypeName_enUS",db.String(100))
	RpAccTypeDesc_enUS = db.Column("RpAccTypeDesc_enUS",db.String(500))
	Rp_acc = db.relationship("Rp_acc",backref='rp_acc_type',lazy=True)

	def to_json_api(self):
		json_data = {
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
		return json_data


class Device(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_device"
	DevId = db.Column("DevId",db.Integer,nullable=False,primary_key=True)
	DevGuid = db.Column("DevGuid",UUID(as_uuid=True),unique=True)
	DevUniqueId = db.Column("DevUniqueId",db.String(100),nullable=False)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	DevName = db.Column("DevName",db.String(200))
	DevDesc = db.Column("DevDesc",db.String(500))
	IsAllowed = db.Column("IsAllowed",db.Boolean,default=False)
	DevVerifyDate = db.Column("DevVerifyDate",db.DateTime,default=datetime.now())
	DevVerifyKey = db.Column("DevVerifyKey",db.String(255))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"DevId": self.DevId,
			"DevGuid": self.DevGuid,
			"DevUniqueId": self.DevUniqueId,
			"RpAccId": self.RpAccId,
			"DevName": self.DevName,
			"DevDesc": self.DevDesc,
			"IsAllowed": self.IsAllowed,
			"DevVerifyDate": apiDataFormat(self.DevVerifyDate),
			"DevVerifyKey": self.DevVerifyKey,
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
		return json_data