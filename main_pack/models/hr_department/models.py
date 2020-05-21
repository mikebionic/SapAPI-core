from flask import json
from main_pack import db
from datetime import datetime
from main_pack.models.base.models import CreatedModifiedInfo, AddInf

class Employee(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_employee"
	EmpId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	ContractTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_contract_type.ContractTypeId"))
	DeptId = db.Column(db.Integer,db.ForeignKey("tbl_dk_department.DeptId"))
	ProfessionId = db.Column(db.Integer,db.ForeignKey("tbl_dk_profession.ProfessionId"))
	EmpStatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_emp_status.EmpStatId"))
	EmpRegNo = db.Column(db.String(128),nullable=False)
	EmpName = db.Column(db.String(255),nullable=False)
	EmpLastName = db.Column(db.String(50))
	EmpFirstName = db.Column(db.String(50))
	EmpPatronymic = db.Column(db.String(50))
	GenderId = db.Column(db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	EmpBirthDate = db.Column(db.DateTime(50))
	EmpBirthPlace = db.Column(db.String(500))
	EmpResidency = db.Column(db.String(500))
	NatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_nationality.NatId"))
	EmpPassportNo = db.Column(db.String(30))
	EmpPaspIssuePlace = db.Column(db.String(255))
	EduLevelId = db.Column(db.Integer,db.ForeignKey("tbl_dk_edu_level.EduLevelId"))
	EmpLangSkills = db.Column(db.String(500))
	MobilePhoneNumber = db.Column(db.String(100))
	HomePhoneNumber = db.Column(db.String(100))
	WorkPhoneNumber = db.Column(db.String(100))
	WorkFaxNumber = db.Column(db.String(100))
	ZipCode = db.Column(db.String(100))
	EMail = db.Column(db.String(100))
	Contact = db.relationship('Contact',backref='employee',lazy=True)
	Location = db.relationship('Location',backref='employee',lazy=True)
	Award = db.relationship('Award',backref='employee',lazy=True)
	Relatives = db.relationship('Relatives',backref='employee',lazy=True)
	School = db.relationship('School',backref='employee',lazy=True)
	Visited_countries = db.relationship('Visited_countries',backref='employee',lazy=True)
	Work_history = db.relationship('Work_history',backref='employee',lazy=True)
	Department_detail = db.relationship('Department_detail',backref='employee',lazy=True)
	Image = db.relationship('Image',backref='employee',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='employee',lazy=True)
	Invoice = db.relationship('Invoice',backref='employee',lazy=True)
	Order_inv = db.relationship('Order_inv',backref='employee',lazy=True)
	Res_trans_inv = db.relationship('Res_trans_inv',backref='employee',lazy=True)
	Rating = db.relationship('Rating',backref='employee',lazy=True)
	# function updates db ignoring Null
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_employee = {
			'empId': self.EmpId,
			'company': self.CId,
			'contractType': self.ContractTypeId,
			'department': self.DeptId,
			'profession': self.ProfessionId,
			'workStatus': self.EmpStatId,
			'regNo': self.EmpRegNo,
			'name': self.EmpName,
			'lastName': self.EmpLastName,
			'firstName': self.EmpFirstName,
			'patronymicName': self.EmpPatronymic,
			'gender': self.GenderId,
			'birthDate': self.EmpBirthDate,
			'birthPlace': self.EmpBirthPlace,
			'residency': self.EmpResidency,
			'nationality': self.NatId,
			'passportNo': self.EmpPassportNo,
			'paspIssuePlace': self.EmpPaspIssuePlace,
			'educationLevel': self.EduLevelId,
			'languageSkills': self.EmpLangSkills,
			'mobilePhone': self.MobilePhoneNumber,
			'homePhone': self.HomePhoneNumber,
			'workPhone': self.WorkPhoneNumber,
			'fax': self.WorkFaxNumber,
			'zipCode': self.ZipCode,
			'email': self.EMail
		}
		return json_employee

class Award(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_award"
	AwardId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	AwardName = db.Column(db.String(100),nullable=False)
	AwardDesc = db.Column(db.String(500))
	AwardRecievedDate = db.Column(db.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_award = {
			'awardId': self.AwardId,
			'empId': self.EmpId,
			'awardName': self.AwardName,
			'awardDesc': self.AwardDesc,
			'awardRecievedDate': self.AwardRecievedDate
		}
		return json_award

class Contract_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contract_type"
	ContractTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	ContractTypeName_tkTM = db.Column(db.String(100))
	ContractTypeDesc_tkTM = db.Column(db.String(100))
	ContractTypeName_ruRU = db.Column(db.String(100))
	ContractTypeDesc_ruRU = db.Column(db.String(100))
	ContractTypeName_enUS = db.Column(db.String(100))
	ContractTypeDesc_enUS = db.Column(db.String(100))
	Employee = db.relationship('Employee',backref='contract_type',lazy=True)
	
	def to_json(self):
		json_contactType = {
			'ContractTypeId': self.ContractTypeId,
			'ContractTypeName_tkTM': self.ContractTypeName_tkTM,
			'ContractTypeDesc_tkTM': self.ContractTypeDesc_tkTM,
			'ContractTypeName_ruRU': self.ContractTypeName_ruRU,
			'ContractTypeDesc_ruRU': self.ContractTypeDesc_ruRU,
			'ContractTypeName_enUS': self.ContractTypeName_enUS,
			'ContractTypeDesc_enUS': self.ContractTypeDesc_enUS
		}
		return json_contactType

class Edu_level(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_edu_level"
	EduLevelId = db.Column(db.Integer,nullable=False,primary_key=True)
	EduLevelName_tkTM = db.Column(db.String(100))#nullable??
	EduLevelDesc_tkTM = db.Column(db.String(500))
	EduLevelName_ruRU = db.Column(db.String(100))#
	EduLevelDesc_ruRU = db.Column(db.String(500))
	EduLevelName_enUS = db.Column(db.String(100))#
	EduLevelDesc_enUS = db.Column(db.String(500))
	Employee = db.relationship('Employee',backref='edu_level',lazy=True)

	def to_json(self):
		json_eduLevel = {
			'EduLevelId': self.EduLevelId,
			'EduLevelName_tkTM': self.EduLevelName_tkTM,
			'EduLevelDesc_tkTM': self.EduLevelDesc_tkTM,
			'EduLevelName_ruRU': self.EduLevelName_ruRU,
			'EduLevelDesc_ruRU': self.EduLevelDesc_ruRU,
			'EduLevelName_enUS': self.EduLevelName_enUS,
			'EduLevelDesc_enUS': self.EduLevelDesc_enUS
		}
		return json_eduLevel
	
class Emp_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_emp_status"
	EmpStatId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpStatName_tkTM = db.Column(db.String(100))#,nullable=False)
	EmpStatDesc_tkTM = db.Column(db.String(500))
	EmpStatName_ruRU = db.Column(db.String(100))#,nullable=False)
	EmpStatDesc_ruRU = db.Column(db.String(500))
	EmpStatName_enUS = db.Column(db.String(100))#,nullable=False)
	EmpStatDesc_enUS = db.Column(db.String(500))
	Employee = db.relationship('Employee',backref='emp_status',lazy=True)

	def to_json(self):
		json_empStatus = {
			'EmpStatId': self.EmpStatId,
			'EmpStatName_tkTM': self.EmpStatName_tkTM,
			'EmpStatDesc_tkTM': self.EmpStatDesc_tkTM,
			'EmpStatName_ruRU': self.EmpStatName_ruRU,
			'EmpStatDesc_ruRU': self.EmpStatDesc_ruRU,
			'EmpStatName_enUS': self.EmpStatName_enUS,
			'EmpStatDesc_enUS': self.EmpStatDesc_enUS
		}
		return json_empStatus

class Nationality(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_nationality"
	NatId = db.Column(db.Integer,nullable=False,primary_key=True)
	NatName_tkTM = db.Column(db.String(50))#,nullable=False)
	NatDesc_tkTM = db.Column(db.String(500))
	NatName_ruRU = db.Column(db.String(50))#,nullable=False)
	NatDesc_ruRU = db.Column(db.String(500))
	NatName_enUS = db.Column(db.String(50))#,nullable=False)
	NatDesc_enUS = db.Column(db.String(500))
	Employee = db.relationship('Employee',backref='nationality',lazy=True)
	Rp_acc = db.relationship('Rp_acc',backref='nationality',lazy=True)

	def to_json(self):
		json_nationality = {
			'NatId': self.NatId,
			'NatName_tkTM': self.NatName_tkTM,
			'NatDesc_tkTM': self.NatDesc_tkTM,
			'NatName_ruRU': self.NatName_ruRU,
			'NatDesc_ruRU': self.NatDesc_ruRU,
			'NatName_enUS': self.NatName_enUS,
			'NatDesc_enUS': self.NatDesc_enUS
		}
		return json_nationality

class Profession(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_profession"
	ProfessionId = db.Column(db.Integer,nullable=False,primary_key=True)
	ProfessionName_tkTM = db.Column(db.String(50))#,nullable=False)
	ProfessionDesc_tkTM = db.Column(db.String(500))
	ProfessionName_ruRU = db.Column(db.String(50))#,nullable=False)
	ProfessionDesc_ruRU = db.Column(db.String(500))
	ProfessionName_enUS = db.Column(db.String(50))#,nullable=False)
	ProfessionDesc_enUS = db.Column(db.String(500))
	Employee = db.relationship('Employee',backref='profession',lazy=True)

	def to_json(self):
		json_profession = {
			'ProfessionId': self.ProfessionId,
			'ProfessionName_tkTM': self.ProfessionName_tkTM,
			'ProfessionDesc_tkTM': self.ProfessionDesc_tkTM,
			'ProfessionName_ruRU': self.ProfessionName_ruRU,
			'ProfessionDesc_ruRU': self.ProfessionDesc_ruRU,
			'ProfessionName_enUS': self.ProfessionName_enUS,
			'ProfessionDesc_enUS': self.ProfessionDesc_enUS
		}
		return json_profession

class Rel_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rel_status"
	RelStatId = db.Column(db.Integer,nullable=False,primary_key=True)
	RelStatName_tkTM = db.Column(db.String(50))#,nullable=False)
	RelStatDesc_tkTM = db.Column(db.String(500))
	RelStatName_ruRU = db.Column(db.String(50))#,nullable=False)
	RelStatDesc_ruRU = db.Column(db.String(500))
	RelStatName_enUS = db.Column(db.String(50))#,nullable=False)
	RelStatDesc_enUS = db.Column(db.String(500))
	Relatives = db.relationship('Relatives',backref='rel_status',lazy=True)

	def to_json(self):
		json_relStatus = {
			'RelStatId': self.RelStatId,
			'RelStatName_tkTM': self.RelStatName_tkTM,
			'RelStatDesc_tkTM': self.RelStatDesc_tkTM,
			'RelStatName_ruRU': self.RelStatName_ruRU,
			'RelStatDesc_ruRU': self.RelStatDesc_ruRU,
			'RelStatName_enUS': self.RelStatName_enUS,
			'RelStatDesc_enUS': self.RelStatDesc_enUS
		}
		return json_relStatus

class Relatives(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_relatives"
	RelId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RelStatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rel_status.RelStatId"))
	RelPersonName = db.Column(db.String(100),nullable=False)
	GenderId = db.Column(db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	RelBirthDate = db.Column(db.DateTime)
	RelBirthPlace = db.Column(db.String(255))
	RelWorkPlace = db.Column(db.String(255))
	RelWorkPosition = db.Column(db.String(255))
	RelResidence = db.Column(db.String(255))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_relatives = {
			'relativesId': self.RelId,
			'empId': self.EmpId,
			'relativesStatus': self.RelStatId,
			'relativesName': self.RelPersonName,
			'relativesGender': self.GenderId,
			'relativesBirthDate': self.RelBirthDate,
			'relativesBirthPlace': self.RelBirthPlace,
			'relativesWorkPlace': self.RelWorkPlace,
			'relativesWorkPosition': self.RelWorkPosition,
			'relativesResidence': self.RelResidence
		}
		return json_relatives

class School(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_school"
	SchoolId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	SchoolTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_school_type.SchoolTypeId"))
	SchoolName = db.Column(db.String(255),nullable=False)
	SchoolDesc = db.Column(db.String(500))
	SchoolPlace = db.Column(db.String(255))
	SchoolEduStartDate = db.Column(db.DateTime)
	SchoolEduEndDate = db.Column(db.DateTime)
	SchoolProfession = db.Column(db.String(255))
	SchoolIsGraduated = db.Column(db.Boolean,default=False)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_school = {
			'schoolId': self.SchoolId,
			'empId': self.EmpId,
			'schoolType': self.SchoolTypeId,
			'schoolName': self.SchoolName,
			'schoolDesc': self.SchoolDesc,
			'schoolPlace': self.SchoolPlace,
			'eduStartDate': self.SchoolEduStartDate,
			'eduEndDate': self.SchoolEduEndDate,
			'schoolProfession': self.SchoolProfession,
			'isGraduated': self.SchoolIsGraduated
		}
		return json_school
	
class School_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_school_type"
	SchoolTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	SchoolTypeName_tkTM = db.Column(db.String(50))#,nullable=False)
	SchoolTypeDesc_tkTM = db.Column(db.String(500))
	SchoolTypeName_ruRU = db.Column(db.String(50))#,nullable=False)
	SchoolTypeDesc_ruRU = db.Column(db.String(500))
	SchoolTypeName_enUS = db.Column(db.String(50))#,nullable=False)
	SchoolTypeDesc_enUS = db.Column(db.String(500))	

class Visited_countries(AddInf,CreatedModifiedInfo,db.Model):   #changed !!!!!!!!!!!!!
	__tablename__="tbl_dk_visited_countries"
	VCId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	VCCountryName = db.Column(db.String(50),nullable=False)
	VCCountryDesc = db.Column(db.String(500))
	VCPurpose = db.Column(db.String(500))
	VCStartDate = db.Column(db.DateTime)
	VCEndDate = db.Column(db.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_vc = {
			'vcId': self.VCId,
			'empId': self.EmpId,
			'vcCountryName': self.VCCountryName,
			'vcCountryDesc': self.VCCountryDesc,
			'vcPurpose': self.VCPurpose,
			'vcStartDate': self.VCStartDate,
			'vcEndDate': self.VCEndDate
		}
		return json_vc

class Work_history(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_work_history"
	WorkHistId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	WorkHistoryWorkPlace = db.Column(db.String(100),nullable=False)
	WorkHistoryWorkDesc = db.Column(db.String(500))
	WorkHistoryWorkDept = db.Column(db.String(255))
	WorkHistoryWorkPos = db.Column(db.String(255))
	WorkHistoryWorkStartDate = db.Column(db.DateTime)
	WorkHistoryWorkEndDate = db.Column(db.DateTime)
	WorkHistoryWorkEndReason = db.Column(db.String(500))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_workHistory = {
			'workHistId': self.WorkHistId,
			'empId': self.EmpId,
			'whWorkPlace': self.WorkHistoryWorkPlace,
			'whWorkDesc': self.WorkHistoryWorkDesc,
			'whWorkDept': self.WorkHistoryWorkDept,
			'whWorkPos': self.WorkHistoryWorkPos,
			'whWorkStartDate': self.WorkHistoryWorkStartDate,
			'whWorkEndDate': self.WorkHistoryWorkEndDate,
			'whWorkEndReason': self.WorkHistoryWorkEndReason,
		}
		return json_workHistory

