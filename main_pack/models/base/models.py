from main_pack import db
from datetime import datetime
from main_pack.base.dataMethods import apiDataFormat,apiCheckImageByte
from sqlalchemy.dialects.postgresql import UUID
from main_pack.base.apiMethods import fileToURL


class CreatedModifiedInfo(object):
	CreatedDate = db.Column("CreatedDate",db.DateTime,default=datetime.now())
	ModifiedDate = db.Column("ModifiedDate",db.DateTime,default=datetime.now(),onupdate=datetime.now())
	SyncDateTime = db.Column("SyncDateTime",db.DateTime,default=datetime.now())
	CreatedUId = db.Column("CreatedUId",db.Integer)
	ModifiedUId = db.Column("ModifiedUId",db.Integer)
	GCRecord = db.Column("GCRecord",db.Integer)

	def createdInfo(self,UId):
		self.CreatedUId = UId

	def modifiedInfo(self,UId):
		self.ModifiedDate = datetime.now()
		self.ModifiedUId = UId


class AddInf(object):
	AddInf1 = db.Column("AddInf1",db.String(500))
	AddInf2 = db.Column("AddInf2",db.String(500))
	AddInf3 = db.Column("AddInf3",db.String(500))
	AddInf4 = db.Column("AddInf4",db.String(500))
	AddInf5 = db.Column("AddInf5",db.String(500))
	AddInf6 = db.Column("AddInf6",db.String(500))


class Acc_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_acc_type"
	AccTypeId = db.Column("AccTypeId",db.Integer,primary_key=True)
	AccTypeName_tkTM = db.Column("AccTypeName_tkTM",db.String(100))
	AccTypeDesc_tkTm = db.Column("AccTypeDesc_tkTm",db.String(500))
	AccTypeName_ruRU = db.Column("AccTypeName_ruRU",db.String(100))
	AccTypeDesc_ruRU = db.Column("AccTypeDesc_ruRU",db.String(500))
	AccTypeName_enUS = db.Column("AccTypeName_enUS",db.String(100))
	AccTypeDesc_enUS = db.Column("AccTypeDesc_enUS",db.String(500))
	Accounting_info = db.relationship('Accounting_info',backref='acc_type',lazy=True)


class Accounting_info(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_accounting_info"
	AccInfId = db.Column("AccInfId",db.Integer,primary_key=True,nullable=False)
	DivisionId = db.Column("DivisionId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	BankId = db.Column("BankId",db.Integer, db.ForeignKey("tbl_dk_bank.BankId"))
	CurrencyId = db.Column("CurrencyId",db.Integer, db.ForeignKey("tbl_dk_currency.CurrencyId"))
	AccTypeId = db.Column("AccTypeId",db.Integer, db.ForeignKey("tbl_dk_acc_type.AccTypeId"))
	CId = db.Column("CId",db.Integer, db.ForeignKey("tbl_dk_company.CId"))
	RpAccId = db.Column("RpAccId",db.Integer, db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	AccInfName = db.Column("AccInfName",db.String(100),nullable=False)
	AccInfDesc = db.Column("AccInfDesc",db.String(500))
	AccInfNo = db.Column("AccInfNo",db.String(50),nullable=False)
	AccInfActive = db.Column("AccInfActive",db.Boolean,default=False)
	AccInfCreatedDate = db.Column("AccInfCreatedDate",db.DateTime)
	AccInfClosedDate = db.Column("AccInfClosedDate",db.DateTime)
	# Company = db.relationship('Company',backref='accounting_info',lazy=True)


class AdditionalInf1(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf1"
	AddInf1Id = db.Column("AddInf1Id",db.Integer,nullable=False,primary_key=True)
	AddInf1Name = db.Column("AddInf1Name",db.String(100),nullable=False)
	AddInf1Desc = db.Column("AddInf1Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class AdditionalInf2(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf2"
	AddInf2Id = db.Column("AddInf2Id",db.Integer,nullable=False,primary_key=True)
	AddInf2Name = db.Column("AddInf2Name",db.String(100),nullable=False)
	AddInf2Desc = db.Column("AddInf2Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class AdditionalInf3(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf3"
	AddInf3Id = db.Column("AddInf3Id",db.Integer,nullable=False,primary_key=True)
	AddInf3Name = db.Column("AddInf3Name",db.String(100),nullable=False)
	AddInf3Desc = db.Column("AddInf3Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class AdditionalInf4(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf4"
	AddInf4Id = db.Column("AddInf4Id",db.Integer,nullable=False,primary_key=True)
	AddInf4Name = db.Column("AddInf4Name",db.String(100),nullable=False)
	AddInf4Desc = db.Column("AddInf4Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class AdditionalInf5(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf5"
	AddInf5Id = db.Column("AddInf5Id",db.Integer,nullable=False,primary_key=True)
	AddInf5Name = db.Column("AddInf5Name",db.String(100),nullable=False)
	AddInf5Desc = db.Column("AddInf5Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class AdditionalInf6(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf6"
	AddInf6Id = db.Column("AddInf6Id",db.Integer,nullable=False,primary_key=True)
	AddInf6Name = db.Column("AddInf6Name",db.String(100),nullable=False)
	AddInf6Desc = db.Column("AddInf6Desc",db.String(500))
	AddInfTypeId = db.Column("AddInfTypeId",db.Integer,default=0)


class Bank(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_bank"
	BankId = db.Column("BankId",db.Integer,nullable=False,primary_key=True)
	MainContId = db.Column("MainContId",db.Integer,default=0)
	MainLocId = db.Column("MainLocId",db.Integer,default=0)
	BankName = db.Column("BankName",db.String(200),nullable=False)
	BankDesc = db.Column("BankDesc",db.String(500))
	BankCorAcc = db.Column("BankCorAcc",db.String(50))
	BankAccBik = db.Column("BankAccBik",db.String(50))
	Accounting_info = db.relationship('Accounting_info',backref='bank',lazy=True)
	Contact = db.relationship('Contact',backref='bank',lazy=True)
	Location = db.relationship('Location',backref='bank',lazy=True)


class City(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_city"
	CityId = db.Column("CityId",db.Integer,nullable=False,primary_key=True)
	CountryId = db.Column("CountryId",db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityName = db.Column("CityName",db.String(50),nullable=False)
	CityDesc = db.Column("CityDesc",db.String(500))
	Location = db.relationship('Location',backref='city',lazy=True)


class Company(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_company"
	CId = db.Column("CId",db.Integer,primary_key=True)
	CName = db.Column("CName",db.String(100),nullable=False)
	CFullName = db.Column("CFullName",db.String(500))
	CDesc = db.Column("CDesc",db.String(500))
	CGuid = db.Column("CGuid",UUID(as_uuid=True),unique=True)
	AccInfId = db.Column("AccInfId",db.Integer)
	CAddress = db.Column("CAddress",db.String(500))
	CAddressLegal = db.Column("CAddressLegal",db.String(500))
	CLatitude = db.Column("CLatitude",db.Float)
	CLongitude = db.Column("CLongitude",db.Float)
	Phone1 = db.Column("Phone1",db.String(100))
	Phone2 = db.Column("Phone2",db.String(100))
	Phone3 = db.Column("Phone3",db.String(100))
	Phone4 = db.Column("Phone4",db.String(100))
	CPostalCode = db.Column("CPostalCode",db.String(100))
	WebAddress = db.Column("WebAddress",db.String(100))
	CEmail = db.Column("CEmail",db.String(100))
	Accounting_info = db.relationship('Accounting_info',backref='company',lazy=True)
	Contact = db.relationship('Contact',backref='company',lazy=True)
	Division = db.relationship('Division',backref='company',lazy=True)
	Image = db.relationship('Image',backref='company',lazy=True)
	Location = db.relationship('Location',backref='company',lazy=True)
	Department_detail = db.relationship('Department_detail',backref='company',lazy=True)
	Warehouse = db.relationship('Warehouse',backref='company',lazy=True)
	Barcode = db.relationship('Barcode',backref='company',lazy=True)
	Rp_acc_transaction = db.relationship('Rp_acc_transaction',backref='company',lazy=True)
	Sale_card = db.relationship('Sale_card',backref='company',lazy=True)
	Work_period = db.relationship('Work_period',backref='company',lazy=True)
	Invoice = db.relationship('Invoice',backref='company',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='company',lazy=True)
	Representative = db.relationship('Representative',backref='company',lazy=True)
	Res_total = db.relationship('Res_total',backref='company',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',backref='company',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='company',lazy=True)
	Users = db.relationship('Users',backref='company',lazy=True)
	Wish = db.relationship('Wish',backref='company',lazy=True)
	Production = db.relationship('Production',backref='company',lazy=True)
	Resource = db.relationship('Resource',backref='company',lazy=True)
	Rating = db.relationship('Rating',backref='company',lazy=True)
	Slider = db.relationship('Slider',backref='company',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_company = {
			"CId": self.CId,
			"CName": self.CName,
			"CFullName": self.CFullName,
			"CDesc": self.CDesc,
			"CGuid": self.CGuid,
			"AccInfId": self.AccInfId,
			"CAddress": self.CAddress,
			"CAddressLegal": self.CAddressLegal,
			"CLatitude": self.CLatitude,
			"CLongitude": self.CLongitude,
			"Phone1": self.Phone1,
			"Phone2": self.Phone2,
			"Phone3": self.Phone3,
			"Phone4": self.Phone4,
			"CPostalCode": self.CPostalCode,
			"WebAddress": self.WebAddress,
			"CEmail": self.CEmail,
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
		return json_company


class Config(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_config"
	CfId = db.Column("CfId",db.Integer,primary_key=True)
	MainCfId = db.Column("MainCfId",db.Integer)
	CfTypeId = db.Column("CfTypeId",db.Integer,db.ForeignKey("tbl_dk_config_type.CfTypeId"))
	CfGuid = db.Column("CfGuid",UUID(as_uuid=True))
	CfName = db.Column("CfName",db.String(100),nullable=False)
	CfDesc = db.Column("CfDesc",db.String(500))
	CfIntVal = db.Column("CfIntVal",db.Integer)
	CfStringVal = db.Column("CfStringVal",db.String(500))
	
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_config = {
			"CfId": self.CfId,
			"MainCfId": self.MainCfId,
			"CfTypeId": self.CfTypeId,
			"CfGuid": self.CfGuid,
			"CfName": self.CfName,
			"CfDesc": self.CfDesc,
			"CfIntVal": self.CfIntVal,
			"CfStringVal": self.CfStringVal,
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
		return json_config


class Config_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_config_type"
	CfTypeId = db.Column("CfTypeId",db.Integer,primary_key=True)
	CfTypeName_tkTM = db.Column("CfTypeName_tkTM",db.String(100))
	CfTypeDesc_tkTM = db.Column("CfTypeDesc_tkTM",db.String(500))
	CfTypeName_ruRU = db.Column("CfTypeName_ruRU",db.String(100))
	CfTypeDesc_ruRU = db.Column("CfTypeDesc_ruRU",db.String(500))
	CfTypeName_enUS = db.Column("CfTypeName_enUS",db.String(100))
	CfTypeDesc_enUS = db.Column("CfTypeDesc_enUS",db.String(500))
	Config = db.relationship('Config',backref='config_type',lazy=True)

	def to_json(self):
		json_configType = {
			"CfTypeId": self.CfTypeId,
			"CfTypeName_tkTM": self.CfTypeName_tkTM,
			"CfTypeDesc_tkTM": self.CfTypeDesc_tkTM,
			"CfTypeName_ruRU": self.CfTypeName_ruRU,
			"CfTypeDesc_ruRU": self.CfTypeDesc_ruRU,
			"CfTypeName_enUS": self.CfTypeName_enUS,
			"CfTypeDesc_enUS": self.CfTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_configType


class Contact(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contact"
	ContId = db.Column("ContId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	BankId = db.Column("BankId",db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	ContTypeId = db.Column("ContTypeId",db.Integer,db.ForeignKey("tbl_dk_contact_type.ContTypeId"))
	ContValue = db.Column("ContValue",db.String(200),nullable=False)
	ContDesc = db.Column("ContDesc",db.String(500))


class Contact_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contact_type"
	ContTypeId = db.Column("ContTypeId",db.Integer,nullable=False,primary_key=True)
	ContTypeName_tkTM = db.Column("ContTypeName_tkTM",db.String(100))
	ContTypeDesc_tkTM = db.Column("ContTypeDesc_tkTM",db.String(500))
	ContTypeName_ruRU = db.Column("ContTypeName_ruRU",db.String(100))
	ContTypeDesc_ruRU = db.Column("ContTypeDesc_ruRU",db.String(500))
	ContTypeName_enUS = db.Column("ContTypeName_enUS",db.String(100))
	ContTypeDesc_enUS = db.Column("ContTypeDesc_enUS",db.String(500))
	Contact = db.relationship('Contact',backref='contact_type',lazy=True)

	def to_json(self):
		json_contactType = {
			"ContactTypeId": self.ContactTypeId,
			"ContactTypeName_tkTM": self.ContactTypeName_tkTM,
			"ContactTypeDesc_tkTM": self.ContactTypeDesc_tkTM,
			"ContactTypeName_ruRU": self.ContactTypeName_ruRU,
			"ContactTypeDesc_ruRU": self.ContactTypeDesc_ruRU,
			"ContactTypeName_enUS": self.ContactTypeName_enUS,
			"ContactTypeDesc_enUS": self.ContactTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_contactType


class Country(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_country"
	CountryId = db.Column("CountryId",db.Integer,nullable=False,primary_key=True)
	CountryName = db.Column("CountryName",db.String(50),nullable=False)
	CountryDesc = db.Column("CountryDesc",db.String(500))
	City = db.relationship('City',backref='country',lazy=True)
	Location = db.relationship('Location',backref='country',lazy=True)


class Currency(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_currency"
	CurrencyId = db.Column("CurrencyId",db.Integer,nullable=False,primary_key=True)
	CurrencyName_tkTM = db.Column("CurrencyName_tkTM",db.String(100),nullable=False)
	CurrencyDesc_tkTM = db.Column("CurrencyDesc_tkTM",db.String(500))
	CurrencyName_ruRU = db.Column("CurrencyName_ruRU",db.String(100),nullable=False)
	CurrencyDesc_ruRU = db.Column("CurrencyDesc_ruRU",db.String(500))
	CurrencyName_enUS = db.Column("CurrencyName_enUS",db.String(100),nullable=False)
	CurrencyDesc_enUS = db.Column("CurrencyDesc_enUS",db.String(500))
	CurrencyCode = db.Column("CurrencyCode",db.String(100))
	CurrencySymbol = db.Column("CurrencySymbol",db.String(100))
	Accounting_info = db.relationship('Accounting_info',backref='currency',lazy=True)
	Exc_rate = db.relationship('Exc_rate',backref='currency',lazy=True)
	Inv_line = db.relationship('Inv_line',backref='currency',lazy=True)
	Invoice = db.relationship('Invoice',backref='currency',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='currency',lazy=True)
	Order_inv_line = db.relationship('Order_inv_line',backref='currency',lazy=True)
	Res_price = db.relationship('Res_price',backref='currency',lazy=True)
	Res_total = db.relationship('Res_total',backref='currency',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',backref='currency',lazy=True)
	Res_trans_inv_line = db.relationship('Res_trans_inv_line',backref='currency',lazy=True)
	Res_transaction = db.relationship('Res_transaction',backref='currency',lazy=True)
	Rp_acc_trans_total = db.relationship('Rp_acc_trans_total',backref='currency',lazy=True)
	Rp_acc_transaction = db.relationship('Rp_acc_transaction',backref='currency',lazy=True)
	Sale_agr_res_price = db.relationship('Sale_agr_res_price',backref='currency',lazy=True)
	Sale_agreement = db.relationship('Sale_agreement',backref='currency',lazy=True)
	Sale_card = db.relationship('Sale_card',backref='currency',lazy=True)
	Work_period = db.relationship('Work_period',backref='currency',lazy=True)

	def to_json_api(self):
		json_currency = {
			"CurrencyId": self.CurrencyId,
			"CurrencyName_tkTM": self.CurrencyName_tkTM,
			"CurrencyDesc_tkTM": self.CurrencyDesc_tkTM,
			"CurrencyName_ruRU": self.CurrencyName_ruRU,
			"CurrencyDesc_ruRU": self.CurrencyDesc_ruRU,
			"CurrencyName_enUS": self.CurrencyName_enUS,
			"CurrencyDesc_enUS": self.CurrencyDesc_enUS,
			"CurrencyCode": self.CurrencyCode,
			"CurrencySymbol": self.CurrencySymbol,
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
		return json_currency


class Db_inf(db.Model):
	__tablename__="tbl_dk_db_inf"
	DbInfId = db.Column("DbInfId",db.Integer,nullable=False,primary_key=True)
	DbInfDbVer = db.Column("DbInfDbVer",db.String(100),nullable=False)
	GCRecord = db.Column("GCRecord",db.Integer)


class Department(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_department"
	DeptId = db.Column("DeptId",db.Integer,nullable=False,primary_key=True)
	DeptName = db.Column("DeptName",db.String(100),nullable=False)
	DeptDesc = db.Column("DeptDesc",db.String(500))
	Employee = db.relationship('Employee',backref='department',lazy=True)
	Department_detail = db.relationship('Department_detail',backref='department',lazy=True)


class Department_detail(db.Model):
	__tablename__="tbl_dk_department_detail"
	DeptDetId = db.Column("DeptDetId",db.Integer,nullable=False,primary_key=True)
	DeptId = db.Column("DeptId",db.Integer,db.ForeignKey("tbl_dk_department.DeptId")) #???
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	DeptHeadEmpId = db.Column("DeptHeadEmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))


class Division(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_division"
	DivId = db.Column("DivId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivName = db.Column("DivName",db.String(100),nullable=False)
	DivDesc = db.Column("DivDesc",db.String(500))
	DivGuid = db.Column("DivGuid",UUID(as_uuid=True),unique=True)
	OwnerDivisionId = db.Column("OwnerDivisionId",db.Integer,default=0)
	Users = db.relationship('Users',backref='division')
	Department_detail = db.relationship('Department_detail',backref='division',lazy=True)
	Accounting_info = db.relationship('Accounting_info',backref='division',lazy=True)
	Barcode = db.relationship('Barcode',backref='division',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='division',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',backref='division',lazy=True)
	Rp_acc_transaction = db.relationship('Rp_acc_transaction',backref='division',lazy=True)
	Sale_card = db.relationship('Sale_card',backref='division',lazy=True)
	Work_period = db.relationship('Work_period',backref='division',lazy=True)
	Invoice = db.relationship('Invoice',backref='division',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='division',lazy=True)
	Representative = db.relationship('Representative',backref='division',lazy=True)
	Res_total = db.relationship('Res_total',backref='division',lazy=True)
	Wish = db.relationship('Wish',backref='division',lazy=True)
	Warehouse = db.relationship('Warehouse',backref='division',lazy=True)
	Production = db.relationship('Production',backref='division',lazy=True)
	Rating = db.relationship('Rating',backref='division',lazy=True)
	Resource = db.relationship('Resource',backref='division',lazy=True)
	Slider = db.relationship('Slider',backref='division',lazy=True)
	Employee = db.relationship('Employee',backref='division',lazy=True)
	
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_division = {
			"DivId": self.DivId,
			"CId": self.CId,
			"DivName": self.DivName,
			"DivDesc": self.DivDesc,
			"DivGuid": self.DivGuid,
			"OwnerDivisionId": self.OwnerDivisionId,
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
		return json_division


class Gender(db.Model):
	__tablename__="tbl_dk_gender"
	GenderId = db.Column("GenderId",db.Integer,nullable=False,primary_key=True)
	GenderName_tkTM = db.Column("GenderName_tkTM",db.String(100))
	GenderName_ruRU = db.Column("GenderName_ruRU",db.String(100))
	GenderName_enUS = db.Column("GenderName_enUS",db.String(100))
	Employee = db.relationship('Employee',backref='gender',lazy=True)
	Relatives = db.relationship('Relatives',backref='gender',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='gender',lazy=True)
	Representative = db.relationship('Representative',backref='gender',lazy=True)


class Image(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_image"
	ImgId = db.Column("ImgId",db.Integer,nullable=False,primary_key=True)
	ImgGuid = db.Column("ImgGuid",UUID(as_uuid=True),unique=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	BrandId = db.Column("BrandId",db.Integer,db.ForeignKey("tbl_dk_brand.BrandId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResCatId = db.Column("ResCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	FileName = db.Column("FileName",db.String(100),default="")
	FilePath = db.Column("FilePath",db.String(255))
	FileHash = db.Column("FileHash",db.String(100))
	MinDarkFileName = db.Column("MinDarkFileName",db.String(100),default="")
	MinDarkFilePath = db.Column("MinDarkFilePath",db.String(255),default="")
	MaxDarkFileName = db.Column("MaxDarkFileName",db.String(100),default="")
	MaxDarkFilePath = db.Column("MaxDarkFilePath",db.String(255),default="")
	MinLightFileName = db.Column("MinLightFileName",db.String(100),default="")
	MinLightFilePath = db.Column("MinLightFilePath",db.String(255),default="")
	MaxLightFileName = db.Column("MaxLightFileName",db.String(100),default="")
	MaxLightFilePath = db.Column("MaxLightFilePath",db.String(255),default="")
	Image = db.Column("Image",db.LargeBinary)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_image = {
			"imgId": self.ImgId,
			"empId": self.EmpId,
			"companyId": self.CId,
			"rpAccId": self.RpAccId,
			"resId": self.ResId,
			"fileName": self.FileName,
			"fileHash": self.FileHash,
			"image": self.Image,
		}
		return json_image

	def to_json_api(self):
		json_image = {
			"ImgId": self.ImgId,
			"ImgGuid": self.ImgGuid,
			"EmpId": self.EmpId,
			"BrandId": self.BrandId,
			"CId": self.CId,
			"UId": self.UId,
			"RpAccId": self.RpAccId,
			"ResId": self.ResId,
			"ResCatId": self.ResCatId,
			"ProdId": self.ProdId,
			"FileName": self.FileName,
			"FilePath": fileToURL(file_type='image',file_size='M',file_name=self.FileName),
			"FilePathS": fileToURL(file_type='image',file_size='S',file_name=self.FileName),
			"FilePathM": fileToURL(file_type='image',file_size='M',file_name=self.FileName),
			"FilePathR": fileToURL(file_type='image',file_size='R',file_name=self.FileName),
			"FileHash": self.FileHash,
			"MinDarkFileName": self.MinDarkFileName,			
			"MinDarkFilePath": self.MinDarkFilePath,
			"MaxDarkFileName": self.MaxDarkFileName,
			"MaxDarkFilePath": self.MaxDarkFilePath,
			"MinLightFileName": self.MinLightFileName,
			"MinLightFilePath": self.MinLightFilePath,
			"MaxLightFileName": self.MaxLightFileName,
			"MaxLightFilePath": self.MaxLightFilePath,
			# # "Image": base64.encodebytes(self.Image).decode('ascii'),
			# "Image": apiCheckImageByte(self.Image),
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_image


class Location(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_location"
	LocId = db.Column("LocId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	BankId = db.Column("BankId",db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CountryId = db.Column("CountryId",db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityId = db.Column("CityId",db.Integer,db.ForeignKey("tbl_dk_city.CityId"))
	LocAddress = db.Column("LocAddress",db.String(500),nullable=False)
	LocAddressOffical = db.Column("LocAddressOffical",db.String(500),nullable=False)
	LocAddressReal = db.Column("LocAddressReal",db.String(500),nullable=False)
	LocPostCode = db.Column("LocPostCode",db.String(25))
	LocLatitude = db.Column("LocLatitude",db.Integer)
	LocLongitude = db.Column("LocLongitude",db.Integer)


class Password(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_password"
	PsswId = db.Column("PsswId",db.Integer,nullable=False,primary_key=True)
	PsswUId = db.Column("PsswUId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	PsswTypeId = db.Column("PsswTypeId",db.Integer,db.ForeignKey("tbl_dk_password_type.PsswTypeId"))
	PsswPassHash = db.Column("PsswPassHash",db.String(255))
	PsswPassword= db.Column("PsswPasswor",db.String(100),nullable=False)


class Password_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_password_type"
	PsswTypeId = db.Column("PsswTypeId",db.Integer,nullable=False,primary_key=True)
	PsswTypeName = db.Column("PsswTypeName",db.String(100),nullable=False)
	PsswTypeDesc = db.Column("PsswTypeDesc",db.String(500))
	Password = db.relationship('Password',backref='password_type',lazy=True)


class Language(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_language"
	LangId = db.Column("LangId",db.Integer,nullable=False,primary_key=True)
	LangName = db.Column("LangName",db.String(100),nullable=False)
	LangDesc = db.Column("LangDesc",db.String(500))
	Res_translations = db.relationship('Res_translations',backref='language',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_language = {
			"langId": self.LangId,
			"langName": self.LangName,
			"langDesc": self.LangDesc
		}
		return json_language


class Prog_language(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_prog_language"
	LangId = db.Column("LangId",db.Integer,nullable=False,primary_key=True)
	LangName = db.Column("LangName",db.String(50),nullable=False)
	LangDesc = db.Column("LangDesc",db.String(200))


class Pred_regnum(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_pred_regnum"
	PredRegNumId = db.Column("PredRegNumId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,db.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	RegNum = db.Column("RegNum",db.String(100),nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		pred_regnum = {
			"PredRegNumId": self.PredRegNumId,			
			"RegNumTypeId": self.RegNumTypeId,
			"RegNum": self.RegNum,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return pred_regnum


class Reg_num(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_reg_num"
	RegNumId = db.Column("RegNumId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,db.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	RegNumPrefix = db.Column("RegNumPrefix",db.String(100))
	RegNumLastNum = db.Column("RegNumLastNum",db.Integer,nullable=False)
	RegNumSuffix = db.Column("RegNumSuffix",db.String(100))

	def registerLastNum(self,RegNumLastNum):
		self.RegNumLastNum+=1


class Reg_num_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_reg_num_type"
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeName_tkTM = db.Column("RegNumTypeName_tkTM",db.String(50),nullable=False)
	RegNumTypeDesc_tkTM = db.Column("RegNumTypeDesc_tkTM",db.String(500))
	RegNumTypeName_ruRU = db.Column("RegNumTypeName_ruRU",db.String(50),nullable=False)
	RegNumTypeDesc_ruRU = db.Column("RegNumTypeDesc_ruRU",db.String(500))
	RegNumTypeName_enUS = db.Column("RegNumTypeName_enUS",db.String(50),nullable=False)
	RegNumTypeDesc_enUS = db.Column("RegNumTypeDesc_enUS",db.String(500))
	Reg_num = db.relationship('Reg_num',backref='reg_num_type',lazy='joined')
	Pred_regnum = db.relationship('Pred_regnum',backref='reg_num_type',lazy='joined')


class Report_file(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_report_file"
	RpFileId = db.Column("RpFileId",db.Integer,nullable=False,primary_key=True)
	RpFileTypeId = db.Column("RpFileTypeId",db.Integer,nullable=False,default=0)
	RpFileName = db.Column("RpFileName",db.String(100))
	RpFileDesc = db.Column("RpFileDesc",db.String(100))
	RpFileFileName = db.Column("RpFileFileName",db.String(100))
	RpIsDefault = db.Column("RpIsDefault",db.Boolean,default=False)


class Rp_acc_price_list(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_price_list"
	RpAccPId = db.Column("RpAccPId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	UnitName = db.Column("UnitName",db.String(100))
	ResBarcode = db.Column("ResBarcode",db.String(100),nullable=False)
	ResName = db.Column("ResName",db.String(100),nullable=False)
	ResDesc = db.Column("ResDesc",db.String(500))
	RpAccPValue = db.Column("RpAccPValue",db.Float,default=0)
	RpAccPDesc = db.Column("RpAccPDesc",db.String(500))
	RpAccPStartDate = db.Column("RpAccPStartDate",db.DateTime)
	RpAccPEndDate = db.Column("RpAccPEndDate",db.DateTime)


class Sl_image(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_sl_image"
	SlImgId = db.Column("SlImgId",db.Integer,nullable=False,primary_key=True)
	SlId = db.Column("SlId",db.Integer,db.ForeignKey("tbl_dk_slider.SlId"))
	SlImgTitle = db.Column("SlImgTitle",db.String(100))
	SlImgDesc = db.Column("SlImgDesc",db.String(500),default='')
	# "SlImgMainImg" bytea,
	SlImgMainImgFileName = db.Column("SlImgMainImgFileName",db.String(255),default='')
	SlImgMainImgFilePath = db.Column("SlImgMainImgFilePath",db.String(255),default='')
	SlImgSubImageFileName1 = db.Column("SlImgSubImageFileName1",db.String(255),default='')
	SlImgSubImageFilePath1 = db.Column("SlImgSubImageFilePath1",db.String(255),default='')
	SlImgSubImageFileName2 = db.Column("SlImgSubImageFileName2",db.String(255),default='')
	SlImgSubImageFilePath2 = db.Column("SlImgSubImageFilePath2",db.String(255),default='')
	SlImgSubImageFileName3 = db.Column("SlImgSubImageFileName3",db.String(255),default='')
	SlImgSubImageFilePath3 = db.Column("SlImgSubImageFilePath3",db.String(255),default='')
	SlImgSubImageFileName4 = db.Column("SlImgSubImageFileName4",db.String(255),default='')
	SlImgSubImageFilePath4 = db.Column("SlImgSubImageFilePath4",db.String(255),default='')
	SlImgSubImageFileName5 = db.Column("SlImgSubImageFileName5",db.String(255),default='')
	SlImgSubImageFilePath5 = db.Column("SlImgSubImageFilePath5",db.String(255),default='')
	SlImgStartDate = db.Column("SlImgStartDate",db.DateTime,default=datetime.now)
	SlImgEndDate = db.Column("SlImgEndDate",db.DateTime)
	Translations = db.relationship('Translations',backref='sl_image',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_sl_image = {
			"SlImgId": self.SlImgId,
			"SlId": self.SlId,
			"SlImgTitle": self.SlImgTitle,
			"SlImgDesc": self.SlImgDesc,
			"SlImgMainImgFileName": self.SlImgMainImgFileName,
			"SlImgMainImgFilePathS": fileToURL(file_type="slider",file_size='S',file_name=self.SlImgMainImgFileName),
			"SlImgMainImgFilePathM": fileToURL(file_type="slider",file_size='M',file_name=self.SlImgMainImgFileName),
			"SlImgMainImgFilePathR": fileToURL(file_type="slider",file_size='R',file_name=self.SlImgMainImgFileName),
			"SlImgSubImageFileName1": self.SlImgSubImageFileName1,
			"SlImgSubImageFilePath1": self.SlImgSubImageFilePath1,
			"SlImgSubImageFileName2": self.SlImgSubImageFileName2,
			"SlImgSubImageFilePath2": self.SlImgSubImageFilePath2,
			"SlImgSubImageFileName3": self.SlImgSubImageFileName3,
			"SlImgSubImageFilePath3": self.SlImgSubImageFilePath3,
			"SlImgSubImageFileName4": self.SlImgSubImageFileName4,
			"SlImgSubImageFilePath4": self.SlImgSubImageFilePath4,
			"SlImgSubImageFileName5": self.SlImgSubImageFileName5,
			"SlImgSubImageFilePath5": self.SlImgSubImageFilePath5,
			"SlImgStartDate": apiDataFormat(self.SlImgStartDate),
			"SlImgEndDate": apiDataFormat(self.SlImgEndDate),
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
		return json_sl_image


class Slider(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_slider"
	SlId = db.Column("SlId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	SlName = db.Column("SlName",db.String(100),nullable=False)
	SlDesc = db.Column("SlDesc",db.String(500),default='')
	Sl_image = db.relationship('Sl_image',backref='slider',lazy='joined')

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_slider = {
			"SlId": self.SlId,
			"CId": self.CId,
			"DivId": self.DivId,
			"SlName": self.SlName,
			"SlDesc": self.SlDesc,
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
		return json_slider


class Translations(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_translations"
	TranslId = db.Column("TranslId",db.Integer,nullable=False,primary_key=True)
	ResCatId = db.Column("ResCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ColorId = db.Column("ColorId",db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	SlImgId = db.Column("SlImgId",db.Integer,db.ForeignKey("tbl_dk_sl_image.SlImgId"))
	TransMain = db.Column("TransMain",db.String(500))
	TransDesc = db.Column("TransDesc",db.String(1000))


class Warehouse(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_warehouse"
	WhId = db.Column("WhId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	WhName = db.Column("WhName",db.String(100),nullable=False)
	WhDesc = db.Column("WhDesc",db.String(500))
	WhGuid = db.Column("WhGuid",UUID(as_uuid=True),unique=True)
	Res_transaction = db.relationship('Res_transaction',backref='warehouse',lazy=True)
	Invoice = db.relationship('Invoice',backref='warehouse',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='warehouse',lazy=True)
	Res_total = db.relationship('Res_total',backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',foreign_keys='Res_trans_inv.WhIdIn',backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',foreign_keys='Res_trans_inv.WhIdOut',backref='warehouse',lazy=True)
	Production = db.relationship('Production',foreign_keys='Production.WhIdIn',backref='warehouse',lazy=True)
	Production = db.relationship('Production',foreign_keys='Production.WhIdOut',backref='warehouse',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_warehouse = {
			"WhId": self.WhId,
			"CId": self.CId,
			"DivId": self.DivId,
			"UsageStatusId": self.UsageStatusId,
			"WhName": self.WhName,
			"WhDesc": self.WhDesc,
			"WhGuid": self.WhGuid,
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
		return json_warehouse