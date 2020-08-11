from main_pack import db_test
from datetime import datetime
from main_pack.base.dataMethods import apiDataFormat,apiCheckImageByte

from main_pack.base.apiMethods import fileToURL


class CreatedModifiedInfo(object):
	CreatedDate = db_test.Column(db_test.DateTime,default=datetime.now)
	ModifiedDate = db_test.Column(db_test.DateTime,default=datetime.now,onupdate=datetime.now)
	CreatedUId = db_test.Column(db_test.Integer)
	ModifiedUId = db_test.Column(db_test.Integer)
	GCRecord = db_test.Column(db_test.Integer)

	def createdInfo(self,UId):
		self.CreatedUId = UId

	def modifiedInfo(self,UId):
		self.ModifiedDate = datetime.now()
		self.ModifiedUId = UId


class AddInf(object):
	AddInf1 = db_test.Column(db_test.String(500))
	AddInf2 = db_test.Column(db_test.String(500))
	AddInf3 = db_test.Column(db_test.String(500))
	AddInf4 = db_test.Column(db_test.String(500))
	AddInf5 = db_test.Column(db_test.String(500))
	AddInf6 = db_test.Column(db_test.String(500))


class Acc_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_acc_type"
	__bind_key__ = 'postgres_test'
	AccTypeId = db_test.Column(db_test.Integer,primary_key=True)
	AccTypeName_tkTM = db_test.Column(db_test.String(100))
	AccTypeDesc_tkTm = db_test.Column(db_test.String(500))
	AccTypeName_ruRU = db_test.Column(db_test.String(100))
	AccTypeDesc_ruRU = db_test.Column(db_test.String(500))
	AccTypeName_enUS = db_test.Column(db_test.String(100))
	AccTypeDesc_enUS = db_test.Column(db_test.String(500))
	Accounting_info = db_test.relationship('Accounting_info',backref='acc_type',lazy=True)


class Accounting_info(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_accounting_info"
	__bind_key__ = 'postgres_test'
	AccInfId = db_test.Column(db_test.Integer,primary_key=True,nullable=False)
	DivisionId = BankId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	BankId = db_test.Column(db_test.Integer, db_test.ForeignKey("tbl_dk_bank.BankId"))
	CurrencyId = db_test.Column(db_test.Integer, db_test.ForeignKey("tbl_dk_currency.CurrencyId"))
	AccTypeId = db_test.Column(db_test.Integer, db_test.ForeignKey("tbl_dk_acc_type.AccTypeId"))
	CId = db_test.Column(db_test.Integer, db_test.ForeignKey("tbl_dk_company.CId"))
	RpAccId = db_test.Column(db_test.Integer, db_test.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	AccInfName = db_test.Column(db_test.String(100),nullable=False)
	AccInfDesc = db_test.Column(db_test.String(500))
	AccInfNo = db_test.Column(db_test.String(50),nullable=False)
	AccInfActive = db_test.Column(db_test.Boolean,default=False)
	AccInfCreatedDate = db_test.Column(db_test.DateTime)
	AccInfClosedDate = db_test.Column(db_test.DateTime)
	# Company = db_test.relationship('Company',backref='accounting_info',lazy=True)


class AdditionalInf1(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf1"
	__bind_key__ = 'postgres_test'
	AddInf1Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf1Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf1Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class AdditionalInf2(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf2"
	__bind_key__ = 'postgres_test'
	AddInf2Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf2Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf2Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class AdditionalInf3(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf3"
	__bind_key__ = 'postgres_test'
	AddInf3Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf3Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf3Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class AdditionalInf4(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf4"
	__bind_key__ = 'postgres_test'
	AddInf4Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf4Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf4Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class AdditionalInf5(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf5"
	__bind_key__ = 'postgres_test'
	AddInf5Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf5Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf5Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class AdditionalInf6(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_additional_inf6"
	__bind_key__ = 'postgres_test'
	AddInf6Id = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	AddInf6Name = db_test.Column(db_test.String(100),nullable=False)
	AddInf6Desc = db_test.Column(db_test.String(500))
	AddInfTypeId = db_test.Column(db_test.Integer,default=0)


class Bank(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_bank"
	__bind_key__ = 'postgres_test'
	BankId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	MainContId = db_test.Column(db_test.Integer,default=0)
	MainLocId = db_test.Column(db_test.Integer,default=0)
	BankName = db_test.Column(db_test.String(200),nullable=False)
	BankDesc = db_test.Column(db_test.String(500))
	BankCorAcc = db_test.Column(db_test.String(50))
	BankAccBik = db_test.Column(db_test.String(50))
	Accounting_info = db_test.relationship('Accounting_info',backref='bank',lazy=True)
	Contact = db_test.relationship('Contact',backref='bank',lazy=True)
	Location = db_test.relationship('Location',backref='bank',lazy=True)


class City(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_city"
	__bind_key__ = 'postgres_test'
	CityId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CountryId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_country.CountryId"))
	CityName = db_test.Column(db_test.String(50),nullable=False)
	CityDesc = db_test.Column(db_test.String(500))
	Location = db_test.relationship('Location',backref='city',lazy=True)


class Company(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_company"
	__bind_key__ = 'postgres_test'
	CId = db_test.Column(db_test.Integer,primary_key=True)
	CName = db_test.Column(db_test.String(100),nullable=False)
	CFullName = db_test.Column(db_test.String(500))
	CDesc = db_test.Column(db_test.String(500))
	AccInfId = db_test.Column(db_test.Integer)
	CAddress = db_test.Column(db_test.String(500))
	CAddressLegal = db_test.Column(db_test.String(500))
	CLatitude = db_test.Column(db_test.Float)
	CLongitude = db_test.Column(db_test.Float)
	Phone1 = db_test.Column(db_test.String(100))
	Phone2 = db_test.Column(db_test.String(100))
	Phone3 = db_test.Column(db_test.String(100))
	Phone4 = db_test.Column(db_test.String(100))
	CPostalCode = db_test.Column(db_test.String(100))
	CEmail = db_test.Column(db_test.String(100))
	Accounting_info = db_test.relationship('Accounting_info',backref='company',lazy=True)
	Contact = db_test.relationship('Contact',backref='company',lazy=True)
	Division = db_test.relationship('Division',backref='company',lazy=True)
	Image = db_test.relationship('Image',backref='company',lazy=True)
	Location = db_test.relationship('Location',backref='company',lazy=True)
	Department_detail = db_test.relationship('Department_detail',backref='company',lazy=True)
	Warehouse = db_test.relationship('Warehouse',backref='company',lazy=True)
	Barcode = db_test.relationship('Barcode',backref='company',lazy=True)
	Rp_acc_transaction = db_test.relationship('Rp_acc_transaction',backref='company',lazy=True)
	Sale_card = db_test.relationship('Sale_card',backref='company',lazy=True)
	Work_period = db_test.relationship('Work_period',backref='company',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='company',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='company',lazy=True)
	Representative = db_test.relationship('Representative',backref='company',lazy=True)
	Res_total = db_test.relationship('Res_total',backref='company',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',backref='company',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='company',lazy=True)
	Wish = db_test.relationship('Wish',backref='company',lazy=True)
	Production = db_test.relationship('Production',backref='company',lazy=True)
	Rating = db_test.relationship('Rating',backref='company',lazy=True)
	Slider = db_test.relationship('Slider',backref='company',lazy=True)

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
			"CEmail": self.CEmail,
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
		return json_company


class Contact(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_contact"
	__bind_key__ = 'postgres_test'
	ContId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	BankId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_bank.BankId"))
	ContTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_contact_type.ContTypeId"))
	ContValue = db_test.Column(db_test.String(200),nullable=False)
	ContDesc = db_test.Column(db_test.String(500))


class Contact_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_contact_type"
	__bind_key__ = 'postgres_test'
	ContTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	ContTypeName_tkTM = db_test.Column(db_test.String(100))
	ContTypeDesc_tkTM = db_test.Column(db_test.String(500))
	ContTypeName_ruRU = db_test.Column(db_test.String(100))
	ContTypeDesc_ruRU = db_test.Column(db_test.String(500))
	ContTypeName_enUS = db_test.Column(db_test.String(100))
	ContTypeDesc_enUS = db_test.Column(db_test.String(500))
	Contact = db_test.relationship('Contact',backref='contact_type',lazy=True)

	def to_json(self):
		json_contactType = {
			'ContactTypeId': self.ContactTypeId,
			'ContactTypeName_tkTM': self.ContactTypeName_tkTM,
			'ContactTypeDesc_tkTM': self.ContactTypeDesc_tkTM,
			'ContactTypeName_ruRU': self.ContactTypeName_ruRU,
			'ContactTypeDesc_ruRU': self.ContactTypeDesc_ruRU,
			'ContactTypeName_enUS': self.ContactTypeName_enUS,
			'ContactTypeDesc_enUS': self.ContactTypeDesc_enUS
		}
		return json_contactType


class Country(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_country"
	__bind_key__ = 'postgres_test'
	CountryId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CountryName = db_test.Column(db_test.String(50),nullable=False)
	CountryDesc = db_test.Column(db_test.String(500))
	City = db_test.relationship('City',backref='country',lazy=True)
	Location = db_test.relationship('Location',backref='country',lazy=True)


class Currency(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_currency"
	__bind_key__ = 'postgres_test'
	CurrencyId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CurrencyName_tkTM = db_test.Column(db_test.String(100),nullable=False)
	CurrencyDesc_tkTM = db_test.Column(db_test.String(500))
	CurrencyName_ruRU = db_test.Column(db_test.String(100),nullable=False)
	CurrencyDesc_ruRU = db_test.Column(db_test.String(500))
	CurrencyName_enUS = db_test.Column(db_test.String(100),nullable=False)
	CurrencyDesc_enUS = db_test.Column(db_test.String(500))
	CurrencyCode = db_test.Column(db_test.String(100))
	CurrencySymbol = db_test.Column(db_test.String(100))
	Accounting_info = db_test.relationship('Accounting_info',backref='currency',lazy=True)
	Exc_rate = db_test.relationship('Exc_rate',backref='currency',lazy=True)
	Inv_line = db_test.relationship('Inv_line',backref='currency',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='currency',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='currency',lazy=True)
	Order_inv_line = db_test.relationship('Order_inv_line',backref='currency',lazy=True)
	Res_price = db_test.relationship('Res_price',backref='currency',lazy=True)
	Res_total = db_test.relationship('Res_total',backref='currency',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',backref='currency',lazy=True)
	Res_trans_inv_line = db_test.relationship('Res_trans_inv_line',backref='currency',lazy=True)
	Res_transaction = db_test.relationship('Res_transaction',backref='currency',lazy=True)
	Rp_acc_trans_total = db_test.relationship('Rp_acc_trans_total',backref='currency',lazy=True)
	Rp_acc_transaction = db_test.relationship('Rp_acc_transaction',backref='currency',lazy=True)
	Sale_agr_res_price = db_test.relationship('Sale_agr_res_price',backref='currency',lazy=True)
	Sale_agreement = db_test.relationship('Sale_agreement',backref='currency',lazy=True)
	Sale_card = db_test.relationship('Sale_card',backref='currency',lazy=True)
	Work_period = db_test.relationship('Work_period',backref='currency',lazy=True)

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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_currency


class Db_inf(db_test.Model):
	__tablename__ = "tbl_dk_db_inf"
	__bind_key__ = 'postgres_test'
	DbInfId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	DbInfDbVer = db_test.Column(db_test.String(100),nullable=False)
	GCRecord = db_test.Column(db_test.Integer)


class Department(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_department"
	__bind_key__ = 'postgres_test'
	DeptId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	DeptName = db_test.Column(db_test.String(100),nullable=False)
	DeptDesc = db_test.Column(db_test.String(500))
	Employee = db_test.relationship('Employee',backref='department',lazy=True)
	Department_detail = db_test.relationship('Department_detail',backref='department',lazy=True)


class Department_detail(db_test.Model):
	__tablename__ = "tbl_dk_department_detail"
	__bind_key__ = 'postgres_test'
	DeptDetId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	DeptId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_department.DeptId")) #???
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	DeptHeadEmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))


class Division(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_division"
	__bind_key__ = 'postgres_test'
	DivId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivisionName = db_test.Column(db_test.String(100),nullable=False)
	DivisionDesc = db_test.Column(db_test.String(500))
	OwnerDivisionId = db_test.Column(db_test.Integer,default=0)
	Users = db_test.relationship('Users',backref='division')
	Department_detail = db_test.relationship('Department_detail',backref='division',lazy=True)
	Accounting_info = db_test.relationship('Accounting_info',backref='division',lazy=True)
	Barcode = db_test.relationship('Barcode',backref='division',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='division',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',backref='division',lazy=True)
	Rp_acc_transaction = db_test.relationship('Rp_acc_transaction',backref='division',lazy=True)
	Sale_card = db_test.relationship('Sale_card',backref='division',lazy=True)
	Work_period = db_test.relationship('Work_period',backref='division',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='division',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='division',lazy=True)
	Representative = db_test.relationship('Representative',backref='division',lazy=True)
	Res_total = db_test.relationship('Res_total',backref='division',lazy=True)
	Wish = db_test.relationship('Wish',backref='division',lazy=True)
	Production = db_test.relationship('Production',backref='division',lazy=True)
	Rating = db_test.relationship('Rating',backref='division',lazy=True)
	Slider = db_test.relationship('Slider',backref='division',lazy=True)


class Gender(db_test.Model):
	__tablename__ = "tbl_dk_gender"
	__bind_key__ = 'postgres_test'
	GenderId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	GenderName_tkTM = db_test.Column(db_test.String(100))
	GenderName_ruRU = db_test.Column(db_test.String(100))
	GenderName_enUS = db_test.Column(db_test.String(100))
	Employee = db_test.relationship('Employee',backref='gender',lazy=True)
	Relatives = db_test.relationship('Relatives',backref='gender',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='gender',lazy=True)
	Representative = db_test.relationship('Representative',backref='gender',lazy=True)


class Image(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_image"
	__bind_key__ = 'postgres_test'
	ImgId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	UId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_users.UId"))
	RpAccId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_resource.ResId"))
	FileName = db_test.Column(db_test.String(100))
	FilePath = db_test.Column(db_test.String(255))	
	FileHash = db_test.Column(db_test.String(100))
	Image = db_test.Column(db_test.LargeBinary)

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
			"EmpId": self.EmpId,
			"CId": self.CId,
			"UId": self.UId,
			"RpAccId": self.RpAccId,
			"ResId": self.ResId,
			"FileName": self.FileName,
			'FilePath':fileToURL(file_type='image',file_size='M',file_name=self.FileName,url='commerce_api_test.get_image'),
			'FilePathS':fileToURL(file_type='image',file_size='S',file_name=self.FileName,url='commerce_api_test.get_image'),
			'FilePathM':fileToURL(file_type='image',file_size='M',file_name=self.FileName,url='commerce_api_test.get_image'),
			'FilePathR':fileToURL(file_type='image',file_size='R',file_name=self.FileName,url='commerce_api_test.get_image'),
			# "FileHash": self.FileHash,
			# # "Image": base64.encodebytes(self.Image).decode('ascii'),
			# "Image": apiCheckImageByte(self.Image),
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_image


class Location(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_location"
	__bind_key__ = 'postgres_test'
	LocId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	BankId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_bank.BankId"))
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CountryId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_country.CountryId"))
	CityId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_city.CityId"))
	LocAddress = db_test.Column(db_test.String(500),nullable=False)
	LocAddressOffical = db_test.Column(db_test.String(500),nullable=False)
	LocAddressReal = db_test.Column(db_test.String(500),nullable=False)
	LocPostCode = db_test.Column(db_test.String(25))
	LocLatitude = db_test.Column(db_test.Integer)
	LocLongitude = db_test.Column(db_test.Integer)


class Password(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_password"
	__bind_key__ = 'postgres_test'
	PsswId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	PsswUId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_users.UId"))
	PsswTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_password_type.PsswTypeId"))
	PsswPassHash = db_test.Column(db_test.String(255))
	PsswPassword= db_test.Column(db_test.String(100),nullable=False)


class Password_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_password_type"
	__bind_key__ = 'postgres_test'
	PsswTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	PsswTypeName = db_test.Column(db_test.String(100),nullable=False)
	PsswTypeDesc = db_test.Column(db_test.String(500))
	Password = db_test.relationship('Password',backref='password_type',lazy=True)


class Language(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_language"
	__bind_key__ = 'postgres_test'
	LangId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	LangName = db_test.Column(db_test.String(100),nullable=False)
	LangDesc = db_test.Column(db_test.String(500))
	Res_translations = db_test.relationship('Res_translations',backref='language',lazy=True)

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


class Prog_language(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_prog_language"
	__bind_key__ = 'postgres_test'
	LangId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	LangName = db_test.Column(db_test.String(50),nullable=False)
	LangDesc = db_test.Column(db_test.String(200))


class Reg_num(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_reg_num"
	__bind_key__ = 'postgres_test'
	RegNumId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	UId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_users.UId"))
	RegNumPrefix = db_test.Column(db_test.String(100))
	RegNumLastNum = db_test.Column(db_test.Integer,nullable=False)
	RegNumSuffix = db_test.Column(db_test.String(100))

	def registerLastNum(self,RegNumLastNum):
		self.RegNumLastNum+=1


class Reg_num_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_reg_num_type"
	__bind_key__ = 'postgres_test'
	RegNumTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RegNumTypeName_tkTM = db_test.Column(db_test.String(50),nullable=False)
	RegNumTypeDesc_tkTM = db_test.Column(db_test.String(500))
	RegNumTypeName_ruRU = db_test.Column(db_test.String(50),nullable=False)
	RegNumTypeDesc_ruRU = db_test.Column(db_test.String(500))
	RegNumTypeName_enUS = db_test.Column(db_test.String(50),nullable=False)
	RegNumTypeDesc_enUS = db_test.Column(db_test.String(500))
	Reg_num = db_test.relationship('Reg_num',backref='reg_num_type',lazy=True)


class Report_file(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_report_file"
	__bind_key__ = 'postgres_test'
	RpFileId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RpFileTypeId = db_test.Column(db_test.Integer,nullable=False,default=0)
	RpFileName = db_test.Column(db_test.String(100))
	RpFileDesc = db_test.Column(db_test.String(100))
	RpFileFileName = db_test.Column(db_test.String(100))
	RpIsDefault = db_test.Column(db_test.Boolean,default=False)


class Rp_acc_price_list(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_rp_acc_price_list"
	__bind_key__ = 'postgres_test'
	RpAccPId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RpAccId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	UnitName = db_test.Column(db_test.String(100))
	ResBarcode = db_test.Column(db_test.String(100),nullable=False)
	ResName = db_test.Column(db_test.String(100),nullable=False)
	ResDesc = db_test.Column(db_test.String(500))
	RpAccPValue = db_test.Column(db_test.Float,default=0)
	RpAccPDesc = db_test.Column(db_test.String(500))
	RpAccPStartDate = db_test.Column(db_test.DateTime)
	RpAccPEndDate = db_test.Column(db_test.DateTime)


class Sl_image(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_sl_image"
	__bind_key__ = 'postgres_test'
	SlImgId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	SlId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_slider.SlId"))
	SlImgName = db_test.Column(db_test.String(100))
	SlImgDesc = db_test.Column(db_test.String(500),default='')
	# "SlImgMainImg" bytea,
	SlImgMainImgFileName = db_test.Column(db_test.String(255),default='')
	SlImgSubImageFileName1 = db_test.Column(db_test.String(500),default='')
	SlImgSubImageFileName2 = db_test.Column(db_test.String(255),default='')
	SlImgSubImageFileName3 = db_test.Column(db_test.String(255),default='')
	SlImgSubImageFileName4 = db_test.Column(db_test.String(255),default='')
	SlImgSubImageFileName5 = db_test.Column(db_test.String(255),default='')
	SlImgStartDate = db_test.Column(db_test.DateTime,default=datetime.now)
	SlImgEndDate = db_test.Column(db_test.DateTime)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_sl_image = {
			"SlImgId": self.SlImgId,
			"SlId": self.SlId,
			"SlImgName": self.SlImgName,
			"SlImgDesc": self.SlImgDesc,
			"SlImgMainImgFileName": fileToURL(file_type="slider",file_size='M',file_name=self.SlImgName),
			'SlImgMainImgFilePathS':fileToURL(file_type="slider",file_size='S',file_name=self.SlImgName),
			'SlImgMainImgFilePathM':fileToURL(file_type="slider",file_size='M',file_name=self.SlImgName),
			'SlImgMainImgFilePathR':fileToURL(file_type="slider",file_size='R',file_name=self.SlImgName),
			"SlImgSubImageFileName1": self.SlImgSubImageFileName1,
			"SlImgSubImageFileName2": self.SlImgSubImageFileName2,
			"SlImgSubImageFileName3": self.SlImgSubImageFileName3,
			"SlImgSubImageFileName4": self.SlImgSubImageFileName4,
			"SlImgSubImageFileName5": self.SlImgSubImageFileName5,
			"SlImgStartDate": self.SlImgStartDate,
			"SlImgEndDate": self.SlImgEndDate,
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
		return json_sl_image


class Slider(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_slider"
	__bind_key__ = 'postgres_test'
	SlId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	SlName = db_test.Column(db_test.String(100),nullable=False)
	SlDesc = db_test.Column(db_test.String(500),default='')
	Sl_image = db_test.relationship('Sl_image',backref='slider',lazy=True)

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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_slider


class Warehouse(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_warehouse"
	__bind_key__ = 'postgres_test'
	WhId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	DivId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_division.DivId"))
	WhName = db_test.Column(db_test.String(100),nullable=False)
	WhDesc = db_test.Column(db_test.String(500))
	Res_transaction = db_test.relationship('Res_transaction',backref='warehouse',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='warehouse',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='warehouse',lazy=True)
	Res_total = db_test.relationship('Res_total',backref='warehouse',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',foreign_keys='Res_trans_inv.WhIdIn',backref='warehouse',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',foreign_keys='Res_trans_inv.WhIdOut',backref='warehouse',lazy=True)
	Production = db_test.relationship('Production',foreign_keys='Production.WhIdIn',backref='warehouse',lazy=True)
	Production = db_test.relationship('Production',foreign_keys='Production.WhIdOut',backref='warehouse',lazy=True)

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
			"WhName": self.WhName,
			"WhDesc": self.WhDesc,
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
		return json_warehouse