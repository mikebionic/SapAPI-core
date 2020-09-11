from main_pack import db
from datetime import datetime
from main_pack.base.dataMethods import apiDataFormat,apiCheckImageByte

from main_pack.base.apiMethods import fileToURL


class CreatedModifiedInfo(object):
	CreatedDate = db.Column(db.DateTime,default=datetime.now())
	ModifiedDate = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
	CreatedUId = db.Column(db.Integer)
	ModifiedUId = db.Column(db.Integer)
	GCRecord = db.Column(db.Integer)

	def createdInfo(self,UId):
		self.CreatedUId = UId

	def modifiedInfo(self,UId):
		self.ModifiedDate = datetime.now()
		self.ModifiedUId = UId


class AddInf(object):
	AddInf1 = db.Column(db.String(500))
	AddInf2 = db.Column(db.String(500))
	AddInf3 = db.Column(db.String(500))
	AddInf4 = db.Column(db.String(500))
	AddInf5 = db.Column(db.String(500))
	AddInf6 = db.Column(db.String(500))


class Acc_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_acc_type"
	AccTypeId = db.Column(db.Integer,primary_key=True)
	AccTypeName_tkTM = db.Column(db.String(100))
	AccTypeDesc_tkTm = db.Column(db.String(500))
	AccTypeName_ruRU = db.Column(db.String(100))
	AccTypeDesc_ruRU = db.Column(db.String(500))
	AccTypeName_enUS = db.Column(db.String(100))
	AccTypeDesc_enUS = db.Column(db.String(500))
	Accounting_info = db.relationship('Accounting_info',backref='acc_type',lazy=True)


class Accounting_info(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_accounting_info"
	AccInfId = db.Column(db.Integer,primary_key=True,nullable=False)
	DivisionId = BankId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	BankId = db.Column(db.Integer, db.ForeignKey("tbl_dk_bank.BankId"))
	CurrencyId = db.Column(db.Integer, db.ForeignKey("tbl_dk_currency.CurrencyId"))
	AccTypeId = db.Column(db.Integer, db.ForeignKey("tbl_dk_acc_type.AccTypeId"))
	CId = db.Column(db.Integer, db.ForeignKey("tbl_dk_company.CId"))
	RpAccId = db.Column(db.Integer, db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	AccInfName = db.Column(db.String(100),nullable=False)
	AccInfDesc = db.Column(db.String(500))
	AccInfNo = db.Column(db.String(50),nullable=False)
	AccInfActive = db.Column(db.Boolean,default=False)
	AccInfCreatedDate = db.Column(db.DateTime)
	AccInfClosedDate = db.Column(db.DateTime)
	# Company = db.relationship('Company',backref='accounting_info',lazy=True)


class AdditionalInf1(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf1"
	AddInf1Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf1Name = db.Column(db.String(100),nullable=False)
	AddInf1Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class AdditionalInf2(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf2"
	AddInf2Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf2Name = db.Column(db.String(100),nullable=False)
	AddInf2Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class AdditionalInf3(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf3"
	AddInf3Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf3Name = db.Column(db.String(100),nullable=False)
	AddInf3Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class AdditionalInf4(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf4"
	AddInf4Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf4Name = db.Column(db.String(100),nullable=False)
	AddInf4Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class AdditionalInf5(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf5"
	AddInf5Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf5Name = db.Column(db.String(100),nullable=False)
	AddInf5Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class AdditionalInf6(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_additional_inf6"
	AddInf6Id = db.Column(db.Integer,nullable=False,primary_key=True)
	AddInf6Name = db.Column(db.String(100),nullable=False)
	AddInf6Desc = db.Column(db.String(500))
	AddInfTypeId = db.Column(db.Integer,default=0)


class Bank(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_bank"
	BankId = db.Column(db.Integer,nullable=False,primary_key=True)
	MainContId = db.Column(db.Integer,default=0)
	MainLocId = db.Column(db.Integer,default=0)
	BankName = db.Column(db.String(200),nullable=False)
	BankDesc = db.Column(db.String(500))
	BankCorAcc = db.Column(db.String(50))
	BankAccBik = db.Column(db.String(50))
	Accounting_info = db.relationship('Accounting_info',backref='bank',lazy=True)
	Contact = db.relationship('Contact',backref='bank',lazy=True)
	Location = db.relationship('Location',backref='bank',lazy=True)


class City(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_city"
	CityId = db.Column(db.Integer,nullable=False,primary_key=True)
	CountryId = db.Column(db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityName = db.Column(db.String(50),nullable=False)
	CityDesc = db.Column(db.String(500))
	Location = db.relationship('Location',backref='city',lazy=True)


class Company(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_company"
	CId = db.Column(db.Integer,primary_key=True)
	CName = db.Column(db.String(100),nullable=False)
	CFullName = db.Column(db.String(500))
	CDesc = db.Column(db.String(500))
	AccInfId = db.Column(db.Integer)
	CAddress = db.Column(db.String(500))
	CAddressLegal = db.Column(db.String(500))
	CLatitude = db.Column(db.Float)
	CLongitude = db.Column(db.Float)
	Phone1 = db.Column(db.String(100))
	Phone2 = db.Column(db.String(100))
	Phone3 = db.Column(db.String(100))
	Phone4 = db.Column(db.String(100))
	CPostalCode = db.Column(db.String(100))
	WebAddress = db.Column(db.String(100))
	CEmail = db.Column(db.String(100))
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
	Wish = db.relationship('Wish',backref='company',lazy=True)
	Production = db.relationship('Production',backref='company',lazy=True)
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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_company


class Contact(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contact"
	ContId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	BankId = db.Column(db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	ContTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_contact_type.ContTypeId"))
	ContValue = db.Column(db.String(200),nullable=False)
	ContDesc = db.Column(db.String(500))


class Contact_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contact_type"
	ContTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	ContTypeName_tkTM = db.Column(db.String(100))
	ContTypeDesc_tkTM = db.Column(db.String(500))
	ContTypeName_ruRU = db.Column(db.String(100))
	ContTypeDesc_ruRU = db.Column(db.String(500))
	ContTypeName_enUS = db.Column(db.String(100))
	ContTypeDesc_enUS = db.Column(db.String(500))
	Contact = db.relationship('Contact',backref='contact_type',lazy=True)

	def to_json(self):
		json_contactType = {
			"ContactTypeId": self.ContactTypeId,
			"ContactTypeName_tkTM": self.ContactTypeName_tkTM,
			"ContactTypeDesc_tkTM": self.ContactTypeDesc_tkTM,
			"ContactTypeName_ruRU": self.ContactTypeName_ruRU,
			"ContactTypeDesc_ruRU": self.ContactTypeDesc_ruRU,
			"ContactTypeName_enUS": self.ContactTypeName_enUS,
			"ContactTypeDesc_enUS": self.ContactTypeDesc_enUS
		}
		return json_contactType


class Country(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_country"
	CountryId = db.Column(db.Integer,nullable=False,primary_key=True)
	CountryName = db.Column(db.String(50),nullable=False)
	CountryDesc = db.Column(db.String(500))
	City = db.relationship('City',backref='country',lazy=True)
	Location = db.relationship('Location',backref='country',lazy=True)


class Currency(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_currency"
	CurrencyId = db.Column(db.Integer,nullable=False,primary_key=True)
	CurrencyName_tkTM = db.Column(db.String(100),nullable=False)
	CurrencyDesc_tkTM = db.Column(db.String(500))
	CurrencyName_ruRU = db.Column(db.String(100),nullable=False)
	CurrencyDesc_ruRU = db.Column(db.String(500))
	CurrencyName_enUS = db.Column(db.String(100),nullable=False)
	CurrencyDesc_enUS = db.Column(db.String(500))
	CurrencyCode = db.Column(db.String(100))
	CurrencySymbol = db.Column(db.String(100))
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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_currency


class Db_inf(db.Model):
	__tablename__="tbl_dk_db_inf"
	DbInfId = db.Column(db.Integer,nullable=False,primary_key=True)
	DbInfDbVer = db.Column(db.String(100),nullable=False)
	GCRecord = db.Column(db.Integer)


class Department(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_department"
	DeptId = db.Column(db.Integer,nullable=False,primary_key=True)
	DeptName = db.Column(db.String(100),nullable=False)
	DeptDesc = db.Column(db.String(500))
	Employee = db.relationship('Employee',backref='department',lazy=True)
	Department_detail = db.relationship('Department_detail',backref='department',lazy=True)


class Department_detail(db.Model):
	__tablename__="tbl_dk_department_detail"
	DeptDetId = db.Column(db.Integer,nullable=False,primary_key=True)
	DeptId = db.Column(db.Integer,db.ForeignKey("tbl_dk_department.DeptId")) #???
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	DeptHeadEmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))


class Division(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_division"
	DivId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivisionName = db.Column(db.String(100),nullable=False)
	DivisionDesc = db.Column(db.String(500))
	OwnerDivisionId = db.Column(db.Integer,default=0)
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
	Production = db.relationship('Production',backref='division',lazy=True)
	Rating = db.relationship('Rating',backref='division',lazy=True)
	Slider = db.relationship('Slider',backref='division',lazy=True)


class Gender(db.Model):
	__tablename__="tbl_dk_gender"
	GenderId = db.Column(db.Integer,nullable=False,primary_key=True)
	GenderName_tkTM = db.Column(db.String(100))
	GenderName_ruRU = db.Column(db.String(100))
	GenderName_enUS = db.Column(db.String(100))
	Employee = db.relationship('Employee',backref='gender',lazy=True)
	Relatives = db.relationship('Relatives',backref='gender',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='gender',lazy=True)
	Representative = db.relationship('Representative',backref='gender',lazy=True)


class Image(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_image"
	ImgId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	BrandId = db.Column(db.Integer,db.ForeignKey("tbl_dk_brand.BrandId"))
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	UId = db.Column(db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	FileName = db.Column(db.String(100))
	FileHash = db.Column(db.String(100))
	FilePath = db.Column(db.String(255))	
	Image = db.Column(db.LargeBinary)

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
			"BrandId": self.BrandId,
			"CId": self.CId,
			"UId": self.UId,
			"RpAccId": self.RpAccId,
			"ResId": self.ResId,
			"FileName": self.FileName,
			"FilePath": fileToURL(file_type='image',file_size='M',file_name=self.FileName),
			"FilePathS": fileToURL(file_type='image',file_size='S',file_name=self.FileName),
			"FilePathM": fileToURL(file_type='image',file_size='M',file_name=self.FileName),
			"FilePathR": fileToURL(file_type='image',file_size='R',file_name=self.FileName),
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


class Location(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_location"
	LocId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	BankId = db.Column(db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CountryId = db.Column(db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityId = db.Column(db.Integer,db.ForeignKey("tbl_dk_city.CityId"))
	LocAddress = db.Column(db.String(500),nullable=False)
	LocAddressOffical = db.Column(db.String(500),nullable=False)
	LocAddressReal = db.Column(db.String(500),nullable=False)
	LocPostCode = db.Column(db.String(25))
	LocLatitude = db.Column(db.Integer)
	LocLongitude = db.Column(db.Integer)


class Password(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_password"
	PsswId = db.Column(db.Integer,nullable=False,primary_key=True)
	PsswUId = db.Column(db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	PsswTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_password_type.PsswTypeId"))
	PsswPassHash = db.Column(db.String(255))
	PsswPassword= db.Column(db.String(100),nullable=False)


class Password_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_password_type"
	PsswTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	PsswTypeName = db.Column(db.String(100),nullable=False)
	PsswTypeDesc = db.Column(db.String(500))
	Password = db.relationship('Password',backref='password_type',lazy=True)


class Language(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_language"
	LangId = db.Column(db.Integer,nullable=False,primary_key=True)
	LangName = db.Column(db.String(100),nullable=False)
	LangDesc = db.Column(db.String(500))
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
	LangId = db.Column(db.Integer,nullable=False,primary_key=True)
	LangName = db.Column(db.String(50),nullable=False)
	LangDesc = db.Column(db.String(200))


class Reg_num(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_reg_num"
	RegNumId = db.Column(db.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	UId = db.Column(db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	RegNumPrefix = db.Column(db.String(100))
	RegNumLastNum = db.Column(db.Integer,nullable=False)
	RegNumSuffix = db.Column(db.String(100))

	def registerLastNum(self,RegNumLastNum):
		self.RegNumLastNum+=1


class Reg_num_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_reg_num_type"
	RegNumTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	RegNumTypeName_tkTM = db.Column(db.String(50),nullable=False)
	RegNumTypeDesc_tkTM = db.Column(db.String(500))
	RegNumTypeName_ruRU = db.Column(db.String(50),nullable=False)
	RegNumTypeDesc_ruRU = db.Column(db.String(500))
	RegNumTypeName_enUS = db.Column(db.String(50),nullable=False)
	RegNumTypeDesc_enUS = db.Column(db.String(500))
	Reg_num = db.relationship('Reg_num',backref='reg_num_type',lazy=True)


class Report_file(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_report_file"
	RpFileId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpFileTypeId = db.Column(db.Integer,nullable=False,default=0)
	RpFileName = db.Column(db.String(100))
	RpFileDesc = db.Column(db.String(100))
	RpFileFileName = db.Column(db.String(100))
	RpIsDefault = db.Column(db.Boolean,default=False)


class Rp_acc_price_list(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_price_list"
	RpAccPId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	UnitName = db.Column(db.String(100))
	ResBarcode = db.Column(db.String(100),nullable=False)
	ResName = db.Column(db.String(100),nullable=False)
	ResDesc = db.Column(db.String(500))
	RpAccPValue = db.Column(db.Float,default=0)
	RpAccPDesc = db.Column(db.String(500))
	RpAccPStartDate = db.Column(db.DateTime)
	RpAccPEndDate = db.Column(db.DateTime)


class Sl_image(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_sl_image"
	SlImgId = db.Column(db.Integer,nullable=False,primary_key=True)
	SlId = db.Column(db.Integer,db.ForeignKey("tbl_dk_slider.SlId"))
	SlImgTitle = db.Column(db.String(100))
	SlImgDesc = db.Column(db.String(500),default='')
	# "SlImgMainImg" bytea,
	SlImgMainImgFileName = db.Column(db.String(255),default='')
	SlImgMainImgFilePath = db.Column(db.String(255),default='')
	SlImgSubImageFileName1 = db.Column(db.String(255),default='')
	SlImgSubImageFilePath1 = db.Column(db.String(255),default='')
	SlImgSubImageFileName2 = db.Column(db.String(255),default='')
	SlImgSubImageFilePath2 = db.Column(db.String(255),default='')
	SlImgSubImageFileName3 = db.Column(db.String(255),default='')
	SlImgSubImageFilePath3 = db.Column(db.String(255),default='')
	SlImgSubImageFileName4 = db.Column(db.String(255),default='')
	SlImgSubImageFilePath4 = db.Column(db.String(255),default='')
	SlImgSubImageFileName5 = db.Column(db.String(255),default='')
	SlImgSubImageFilePath5 = db.Column(db.String(255),default='')
	SlImgStartDate = db.Column(db.DateTime,default=datetime.now)
	SlImgEndDate = db.Column(db.DateTime)
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
			"SlImgMainImgFileName": fileToURL(file_type="slider",file_size='M',file_name=self.SlImgMainImgFileName),
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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_sl_image


class Slider(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_slider"
	SlId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	SlName = db.Column(db.String(100),nullable=False)
	SlDesc = db.Column(db.String(500),default='')
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
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_slider


class Translations(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_translations"
	TranslId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResCatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ColorId = db.Column(db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))
	ProdId = db.Column(db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	SlImgId = db.Column(db.Integer,db.ForeignKey("tbl_dk_sl_image.SlImgId"))
	TransMain = db.Column(db.String(500))
	TransDesc = db.Column(db.String(1000))


class Warehouse(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_warehouse"
	WhId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhName = db.Column(db.String(100),nullable=False)
	WhDesc = db.Column(db.String(500))
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