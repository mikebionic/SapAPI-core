from flask import json
from main_pack import db_test
from datetime import datetime
from main_pack.models_test.base.models import CreatedModifiedInfo, AddInf


class Employee(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_employee"
	__bind_key__ = 'postgres_test'
	EmpId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	CId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_company.CId"))
	ContractTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_contract_type.ContractTypeId"))
	DeptId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_department.DeptId"))
	ProfessionId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_profession.ProfessionId"))
	EmpStatId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_emp_status.EmpStatId"))
	EmpRegNo = db_test.Column(db_test.String(128),nullable=False)
	EmpName = db_test.Column(db_test.String(255),nullable=False)
	EmpLastName = db_test.Column(db_test.String(50))
	EmpFirstName = db_test.Column(db_test.String(50))
	EmpPatronymic = db_test.Column(db_test.String(50))
	GenderId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_gender.GenderId"))
	EmpBirthDate = db_test.Column(db_test.DateTime(50))
	EmpBirthPlace = db_test.Column(db_test.String(500))
	EmpResidency = db_test.Column(db_test.String(500))
	NatId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_nationality.NatId"))
	EmpPassportNo = db_test.Column(db_test.String(30))
	EmpPaspIssuePlace = db_test.Column(db_test.String(255))
	EduLevelId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_edu_level.EduLevelId"))
	EmpLangSkills = db_test.Column(db_test.String(500))
	MobilePhoneNumber = db_test.Column(db_test.String(100))
	HomePhoneNumber = db_test.Column(db_test.String(100))
	WorkPhoneNumber = db_test.Column(db_test.String(100))
	WorkFaxNumber = db_test.Column(db_test.String(100))
	ZipCode = db_test.Column(db_test.String(100))
	EMail = db_test.Column(db_test.String(100))
	Contact = db_test.relationship('Contact',backref='employee',lazy=True)
	Location = db_test.relationship('Location',backref='employee',lazy=True)
	Award = db_test.relationship('Award',backref='employee',lazy=True)
	Relatives = db_test.relationship('Relatives',backref='employee',lazy=True)
	School = db_test.relationship('School',backref='employee',lazy=True)
	Visited_countries = db_test.relationship('Visited_countries',backref='employee',lazy=True)
	Work_history = db_test.relationship('Work_history',backref='employee',lazy=True)
	Department_detail = db_test.relationship('Department_detail',backref='employee',lazy=True)
	Image = db_test.relationship('Image',backref='employee',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='employee',lazy=True)
	Invoice = db_test.relationship('Invoice',backref='employee',lazy=True)
	Order_inv = db_test.relationship('Order_inv',backref='employee',lazy=True)
	Res_trans_inv = db_test.relationship('Res_trans_inv',backref='employee',lazy=True)
	Rating = db_test.relationship('Rating',backref='employee',lazy=True)
	# function updates db ignoring Null
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_employee = {
			"empId": self.EmpId,
			"company": self.CId,
			"contractType": self.ContractTypeId,
			"department": self.DeptId,
			"profession": self.ProfessionId,
			"workStatus": self.EmpStatId,
			"regNo": self.EmpRegNo,
			"name": self.EmpName,
			"lastName": self.EmpLastName,
			"firstName": self.EmpFirstName,
			"patronymicName": self.EmpPatronymic,
			"gender": self.GenderId,
			"birthDate": self.EmpBirthDate,
			"birthPlace": self.EmpBirthPlace,
			"residency": self.EmpResidency,
			"nationality": self.NatId,
			"passportNo": self.EmpPassportNo,
			"paspIssuePlace": self.EmpPaspIssuePlace,
			"educationLevel": self.EduLevelId,
			"languageSkills": self.EmpLangSkills,
			"mobilePhone": self.MobilePhoneNumber,
			"homePhone": self.HomePhoneNumber,
			"workPhone": self.WorkPhoneNumber,
			"fax": self.WorkFaxNumber,
			"zipCode": self.ZipCode,
			"email": self.EMail
		}
		return json_employee


class Award(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_award"
	__bind_key__ = 'postgres_test'
	AwardId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	AwardName = db_test.Column(db_test.String(100),nullable=False)
	AwardDesc = db_test.Column(db_test.String(500))
	AwardRecievedDate = db_test.Column(db_test.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_award = {
			"awardId": self.AwardId,
			"empId": self.EmpId,
			"awardName": self.AwardName,
			"awardDesc": self.AwardDesc,
			"awardRecievedDate": self.AwardRecievedDate
		}
		return json_award


class Contract_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_contract_type"
	__bind_key__ = 'postgres_test'
	ContractTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	ContractTypeName_tkTM = db_test.Column(db_test.String(100))
	ContractTypeDesc_tkTM = db_test.Column(db_test.String(100))
	ContractTypeName_ruRU = db_test.Column(db_test.String(100))
	ContractTypeDesc_ruRU = db_test.Column(db_test.String(100))
	ContractTypeName_enUS = db_test.Column(db_test.String(100))
	ContractTypeDesc_enUS = db_test.Column(db_test.String(100))
	Employee = db_test.relationship('Employee',backref='contract_type',lazy=True)
	
	def to_json(self):
		json_contactType = {
			"ContractTypeId": self.ContractTypeId,
			"ContractTypeName_tkTM": self.ContractTypeName_tkTM,
			"ContractTypeDesc_tkTM": self.ContractTypeDesc_tkTM,
			"ContractTypeName_ruRU": self.ContractTypeName_ruRU,
			"ContractTypeDesc_ruRU": self.ContractTypeDesc_ruRU,
			"ContractTypeName_enUS": self.ContractTypeName_enUS,
			"ContractTypeDesc_enUS": self.ContractTypeDesc_enUS
		}
		return json_contactType


class Edu_level(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_edu_level"
	__bind_key__ = 'postgres_test'
	EduLevelId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EduLevelName_tkTM = db_test.Column(db_test.String(100))#nullable??
	EduLevelDesc_tkTM = db_test.Column(db_test.String(500))
	EduLevelName_ruRU = db_test.Column(db_test.String(100))#
	EduLevelDesc_ruRU = db_test.Column(db_test.String(500))
	EduLevelName_enUS = db_test.Column(db_test.String(100))#
	EduLevelDesc_enUS = db_test.Column(db_test.String(500))
	Employee = db_test.relationship('Employee',backref='edu_level',lazy=True)

	def to_json(self):
		json_eduLevel = {
			"EduLevelId": self.EduLevelId,
			"EduLevelName_tkTM": self.EduLevelName_tkTM,
			"EduLevelDesc_tkTM": self.EduLevelDesc_tkTM,
			"EduLevelName_ruRU": self.EduLevelName_ruRU,
			"EduLevelDesc_ruRU": self.EduLevelDesc_ruRU,
			"EduLevelName_enUS": self.EduLevelName_enUS,
			"EduLevelDesc_enUS": self.EduLevelDesc_enUS
		}
		return json_eduLevel


class Emp_status(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_emp_status"
	__bind_key__ = 'postgres_test'
	EmpStatId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpStatName_tkTM = db_test.Column(db_test.String(100))#,nullable=False)
	EmpStatDesc_tkTM = db_test.Column(db_test.String(500))
	EmpStatName_ruRU = db_test.Column(db_test.String(100))#,nullable=False)
	EmpStatDesc_ruRU = db_test.Column(db_test.String(500))
	EmpStatName_enUS = db_test.Column(db_test.String(100))#,nullable=False)
	EmpStatDesc_enUS = db_test.Column(db_test.String(500))
	Employee = db_test.relationship('Employee',backref='emp_status',lazy=True)

	def to_json(self):
		json_empStatus = {
			"EmpStatId": self.EmpStatId,
			"EmpStatName_tkTM": self.EmpStatName_tkTM,
			"EmpStatDesc_tkTM": self.EmpStatDesc_tkTM,
			"EmpStatName_ruRU": self.EmpStatName_ruRU,
			"EmpStatDesc_ruRU": self.EmpStatDesc_ruRU,
			"EmpStatName_enUS": self.EmpStatName_enUS,
			"EmpStatDesc_enUS": self.EmpStatDesc_enUS
		}
		return json_empStatus


class Nationality(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_nationality"
	__bind_key__ = 'postgres_test'
	NatId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	NatName_tkTM = db_test.Column(db_test.String(50))#,nullable=False)
	NatDesc_tkTM = db_test.Column(db_test.String(500))
	NatName_ruRU = db_test.Column(db_test.String(50))#,nullable=False)
	NatDesc_ruRU = db_test.Column(db_test.String(500))
	NatName_enUS = db_test.Column(db_test.String(50))#,nullable=False)
	NatDesc_enUS = db_test.Column(db_test.String(500))
	Employee = db_test.relationship('Employee',backref='nationality',lazy=True)
	Rp_acc = db_test.relationship('Rp_acc',backref='nationality',lazy=True)

	def to_json(self):
		json_nationality = {
			"NatId": self.NatId,
			"NatName_tkTM": self.NatName_tkTM,
			"NatDesc_tkTM": self.NatDesc_tkTM,
			"NatName_ruRU": self.NatName_ruRU,
			"NatDesc_ruRU": self.NatDesc_ruRU,
			"NatName_enUS": self.NatName_enUS,
			"NatDesc_enUS": self.NatDesc_enUS
		}
		return json_nationality


class Profession(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_profession"
	__bind_key__ = 'postgres_test'
	ProfessionId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	ProfessionName_tkTM = db_test.Column(db_test.String(50))#,nullable=False)
	ProfessionDesc_tkTM = db_test.Column(db_test.String(500))
	ProfessionName_ruRU = db_test.Column(db_test.String(50))#,nullable=False)
	ProfessionDesc_ruRU = db_test.Column(db_test.String(500))
	ProfessionName_enUS = db_test.Column(db_test.String(50))#,nullable=False)
	ProfessionDesc_enUS = db_test.Column(db_test.String(500))
	Employee = db_test.relationship('Employee',backref='profession',lazy=True)

	def to_json(self):
		json_profession = {
			"ProfessionId": self.ProfessionId,
			"ProfessionName_tkTM": self.ProfessionName_tkTM,
			"ProfessionDesc_tkTM": self.ProfessionDesc_tkTM,
			"ProfessionName_ruRU": self.ProfessionName_ruRU,
			"ProfessionDesc_ruRU": self.ProfessionDesc_ruRU,
			"ProfessionName_enUS": self.ProfessionName_enUS,
			"ProfessionDesc_enUS": self.ProfessionDesc_enUS
		}
		return json_profession


class Rel_status(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_rel_status"
	__bind_key__ = 'postgres_test'
	RelStatId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	RelStatName_tkTM = db_test.Column(db_test.String(50))#,nullable=False)
	RelStatDesc_tkTM = db_test.Column(db_test.String(500))
	RelStatName_ruRU = db_test.Column(db_test.String(50))#,nullable=False)
	RelStatDesc_ruRU = db_test.Column(db_test.String(500))
	RelStatName_enUS = db_test.Column(db_test.String(50))#,nullable=False)
	RelStatDesc_enUS = db_test.Column(db_test.String(500))
	Relatives = db_test.relationship('Relatives',backref='rel_status',lazy=True)

	def to_json(self):
		json_relStatus = {
			"RelStatId": self.RelStatId,
			"RelStatName_tkTM": self.RelStatName_tkTM,
			"RelStatDesc_tkTM": self.RelStatDesc_tkTM,
			"RelStatName_ruRU": self.RelStatName_ruRU,
			"RelStatDesc_ruRU": self.RelStatDesc_ruRU,
			"RelStatName_enUS": self.RelStatName_enUS,
			"RelStatDesc_enUS": self.RelStatDesc_enUS
		}
		return json_relStatus


class Relatives(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_relatives"
	__bind_key__ = 'postgres_test'
	RelId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	RelStatId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_rel_status.RelStatId"))
	RelPersonName = db_test.Column(db_test.String(100),nullable=False)
	GenderId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_gender.GenderId"))
	RelBirthDate = db_test.Column(db_test.DateTime)
	RelBirthPlace = db_test.Column(db_test.String(255))
	RelWorkPlace = db_test.Column(db_test.String(255))
	RelWorkPosition = db_test.Column(db_test.String(255))
	RelResidence = db_test.Column(db_test.String(255))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_relatives = {
			"relativesId": self.RelId,
			"empId": self.EmpId,
			"relativesStatus": self.RelStatId,
			"relativesName": self.RelPersonName,
			"relativesGender": self.GenderId,
			"relativesBirthDate": self.RelBirthDate,
			"relativesBirthPlace": self.RelBirthPlace,
			"relativesWorkPlace": self.RelWorkPlace,
			"relativesWorkPosition": self.RelWorkPosition,
			"relativesResidence": self.RelResidence
		}
		return json_relatives


class School(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_school"
	__bind_key__ = 'postgres_test'
	SchoolId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	SchoolTypeId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_school_type.SchoolTypeId"))
	SchoolName = db_test.Column(db_test.String(255),nullable=False)
	SchoolDesc = db_test.Column(db_test.String(500))
	SchoolPlace = db_test.Column(db_test.String(255))
	SchoolEduStartDate = db_test.Column(db_test.DateTime)
	SchoolEduEndDate = db_test.Column(db_test.DateTime)
	SchoolProfession = db_test.Column(db_test.String(255))
	SchoolIsGraduated = db_test.Column(db_test.Boolean,default=False)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_school = {
			"schoolId": self.SchoolId,
			"empId": self.EmpId,
			"schoolType": self.SchoolTypeId,
			"schoolName": self.SchoolName,
			"schoolDesc": self.SchoolDesc,
			"schoolPlace": self.SchoolPlace,
			"eduStartDate": self.SchoolEduStartDate,
			"eduEndDate": self.SchoolEduEndDate,
			"schoolProfession": self.SchoolProfession,
			"isGraduated": self.SchoolIsGraduated
		}
		return json_school


class School_type(CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_school_type"
	__bind_key__ = 'postgres_test'
	SchoolTypeId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	SchoolTypeName_tkTM = db_test.Column(db_test.String(50))#,nullable=False)
	SchoolTypeDesc_tkTM = db_test.Column(db_test.String(500))
	SchoolTypeName_ruRU = db_test.Column(db_test.String(50))#,nullable=False)
	SchoolTypeDesc_ruRU = db_test.Column(db_test.String(500))
	SchoolTypeName_enUS = db_test.Column(db_test.String(50))#,nullable=False)
	SchoolTypeDesc_enUS = db_test.Column(db_test.String(500))	


# !!! changed
class Visited_countries(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_visited_countries"
	__bind_key__ = 'postgres_test'
	VCId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	VCCountryName = db_test.Column(db_test.String(50),nullable=False)
	VCCountryDesc = db_test.Column(db_test.String(500))
	VCPurpose = db_test.Column(db_test.String(500))
	VCStartDate = db_test.Column(db_test.DateTime)
	VCEndDate = db_test.Column(db_test.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_vc = {
			"vcId": self.VCId,
			"empId": self.EmpId,
			"vcCountryName": self.VCCountryName,
			"vcCountryDesc": self.VCCountryDesc,
			"vcPurpose": self.VCPurpose,
			"vcStartDate": self.VCStartDate,
			"vcEndDate": self.VCEndDate
		}
		return json_vc


class Work_history(AddInf,CreatedModifiedInfo,db_test.Model):
	__tablename__ = "tbl_dk_work_history"
	__bind_key__ = 'postgres_test'
	WorkHistId = db_test.Column(db_test.Integer,nullable=False,primary_key=True)
	EmpId = db_test.Column(db_test.Integer,db_test.ForeignKey("tbl_dk_employee.EmpId"))
	WorkHistoryWorkPlace = db_test.Column(db_test.String(100),nullable=False)
	WorkHistoryWorkDesc = db_test.Column(db_test.String(500))
	WorkHistoryWorkDept = db_test.Column(db_test.String(255))
	WorkHistoryWorkPos = db_test.Column(db_test.String(255))
	WorkHistoryWorkStartDate = db_test.Column(db_test.DateTime)
	WorkHistoryWorkEndDate = db_test.Column(db_test.DateTime)
	WorkHistoryWorkEndReason = db_test.Column(db_test.String(500))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_workHistory = {
			"workHistId": self.WorkHistId,
			"empId": self.EmpId,
			"whWorkPlace": self.WorkHistoryWorkPlace,
			"whWorkDesc": self.WorkHistoryWorkDesc,
			"whWorkDept": self.WorkHistoryWorkDept,
			"whWorkPos": self.WorkHistoryWorkPos,
			"whWorkStartDate": self.WorkHistoryWorkStartDate,
			"whWorkEndDate": self.WorkHistoryWorkEndDate,
			"whWorkEndReason": self.WorkHistoryWorkEndReason,
		}
		return json_workHistory