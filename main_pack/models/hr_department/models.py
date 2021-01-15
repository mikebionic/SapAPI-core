from flask import json
from main_pack import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from main_pack.models.base.models import CreatedModifiedInfo, AddInf


class Employee(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_employee"
	EmpId = db.Column("EmpId",db.Integer,nullable=False,primary_key=True)
	EmpGuid = db.Column("EmpGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ContractTypeId = db.Column("ContractTypeId",db.Integer,db.ForeignKey("tbl_dk_contract_type.ContractTypeId"))
	DeptId = db.Column("DeptId",db.Integer,db.ForeignKey("tbl_dk_department.DeptId"))
	ProfessionId = db.Column("ProfessionId",db.Integer,db.ForeignKey("tbl_dk_profession.ProfessionId"))
	EmpStatId = db.Column("EmpStatId",db.Integer,db.ForeignKey("tbl_dk_emp_status.EmpStatId"))
	EmpRegNo = db.Column("EmpRegNo",db.String(128),nullable=False)
	EmpName = db.Column("EmpName",db.String(255),nullable=False)
	EmpLastName = db.Column("EmpLastName",db.String(50))
	EmpFirstName = db.Column("EmpFirstName",db.String(50))
	EmpPatronymic = db.Column("EmpPatronymic",db.String(50))
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	EmpBirthDate = db.Column("EmpBirthDate",db.DateTime(50))
	EmpBirthPlace = db.Column("EmpBirthPlace",db.String(500))
	EmpResidency = db.Column("EmpResidency",db.String(500))
	NatId = db.Column("NatId",db.Integer,db.ForeignKey("tbl_dk_nationality.NatId"))
	EmpPassportNo = db.Column("EmpPassportNo",db.String(30))
	EmpPaspIssuePlace = db.Column("EmpPaspIssuePlace",db.String(255))
	EduLevelId = db.Column("EduLevelId",db.Integer,db.ForeignKey("tbl_dk_edu_level.EduLevelId"))
	EmpLangSkills = db.Column("EmpLangSkills",db.String(500))
	MobilePhoneNumber = db.Column("MobilePhoneNumber",db.String(100))
	HomePhoneNumber = db.Column("HomePhoneNumber",db.String(100))
	WorkPhoneNumber = db.Column("WorkPhoneNumber",db.String(100))
	WorkFaxNumber = db.Column("WorkFaxNumber",db.String(100))
	ZipCode = db.Column("ZipCode",db.String(100))
	EMail = db.Column("EMail",db.String(100))
	Contact = db.relationship("Contact",backref='employee',lazy=True)
	Location = db.relationship("Location",backref='employee',lazy=True)
	Award = db.relationship("Award",backref='employee',lazy=True)
	Relatives = db.relationship("Relatives",backref='employee',lazy=True)
	School = db.relationship("School",backref='employee',lazy=True)
	Visited_countries = db.relationship("Visited_countries",backref='employee',lazy=True)
	Work_history = db.relationship("Work_history",backref='employee',lazy=True)
	Department_detail = db.relationship("Department_detail",backref='employee',lazy=True)
	Image = db.relationship("Image",backref='employee',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='employee',lazy=True)
	Invoice = db.relationship("Invoice",backref='employee',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='employee',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",backref='employee',lazy=True)
	Rating = db.relationship("Rating",backref='employee',lazy=True)
	# function updates db ignoring Null
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_data = {
			"empId": self.EmpId,
			"company": self.CId,
			"DivId": self.DivId,
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
		return json_data

	def to_json_api(self):
		employee = {
			"EmpId": self.EmpId,
			"EmpGuid": self.EmpGuid,
			"CId": self.CId,
			"ContractTypeId": self.ContractTypeId,
			"DeptId": self.DeptId,
			"ProfessionId": self.ProfessionId,
			"EmpStatId": self.EmpStatId,
			"EmpRegNo": self.EmpRegNo,
			"EmpName": self.EmpName,
			"EmpLastName": self.EmpLastName,
			"EmpFirstName": self.EmpFirstName,
			"EmpPatronymic": self.EmpPatronymic,
			"GenderId": self.GenderId,
			"EmpBirthDate": self.EmpBirthDate,
			"EmpBirthPlace": self.EmpBirthPlace,
			"EmpResidency": self.EmpResidency,
			"NatId": self.NatId,
			"EmpPassportNo": self.EmpPassportNo,
			"EmpPaspIssuePlace": self.EmpPaspIssuePlace,
			"EduLevelId": self.EduLevelId,
			"EmpLangSkills": self.EmpLangSkills,
			"MobilePhoneNumber": self.MobilePhoneNumber,
			"HomePhoneNumber": self.HomePhoneNumber,
			"WorkPhoneNumber": self.WorkPhoneNumber,
			"WorkFaxNumber": self.WorkFaxNumber,
			"ZipCode": self.ZipCode,
			"EMail": self.EMail,
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
		return employee


class Award(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_award"
	AwardId = db.Column("AwardId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	AwardName = db.Column("AwardName",db.String(100),nullable=False)
	AwardDesc = db.Column("AwardDesc",db.String(500))
	AwardRecievedDate = db.Column("AwardRecievedDate",db.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
			"awardId": self.AwardId,
			"empId": self.EmpId,
			"awardName": self.AwardName,
			"awardDesc": self.AwardDesc,
			"awardRecievedDate": self.AwardRecievedDate
		}
		return json_data


class Contract_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_contract_type"
	ContractTypeId = db.Column("ContractTypeId",db.Integer,nullable=False,primary_key=True)
	ContractTypeName_tkTM = db.Column("ContractTypeName_tkTM",db.String(100))
	ContractTypeDesc_tkTM = db.Column("ContractTypeDesc_tkTM",db.String(100))
	ContractTypeName_ruRU = db.Column("ContractTypeName_ruRU",db.String(100))
	ContractTypeDesc_ruRU = db.Column("ContractTypeDesc_ruRU",db.String(100))
	ContractTypeName_enUS = db.Column("ContractTypeName_enUS",db.String(100))
	ContractTypeDesc_enUS = db.Column("ContractTypeDesc_enUS",db.String(100))
	Employee = db.relationship("Employee",backref='contract_type',lazy=True)
	
	def to_json(self):
		json_data = {
			"ContractTypeId": self.ContractTypeId,
			"ContractTypeName_tkTM": self.ContractTypeName_tkTM,
			"ContractTypeDesc_tkTM": self.ContractTypeDesc_tkTM,
			"ContractTypeName_ruRU": self.ContractTypeName_ruRU,
			"ContractTypeDesc_ruRU": self.ContractTypeDesc_ruRU,
			"ContractTypeName_enUS": self.ContractTypeName_enUS,
			"ContractTypeDesc_enUS": self.ContractTypeDesc_enUS
		}
		return json_data


class Edu_level(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_edu_level"
	EduLevelId = db.Column("EduLevelId",db.Integer,nullable=False,primary_key=True)
	EduLevelName_tkTM = db.Column("EduLevelName_tkTM",db.String(100))#nullable??
	EduLevelDesc_tkTM = db.Column("EduLevelDesc_tkTM",db.String(500))
	EduLevelName_ruRU = db.Column("EduLevelName_ruRU",db.String(100))#
	EduLevelDesc_ruRU = db.Column("EduLevelDesc_ruRU",db.String(500))
	EduLevelName_enUS = db.Column("EduLevelName_enUS",db.String(100))#
	EduLevelDesc_enUS = db.Column("EduLevelDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='edu_level',lazy=True)

	def to_json(self):
		json_data = {
			"EduLevelId": self.EduLevelId,
			"EduLevelName_tkTM": self.EduLevelName_tkTM,
			"EduLevelDesc_tkTM": self.EduLevelDesc_tkTM,
			"EduLevelName_ruRU": self.EduLevelName_ruRU,
			"EduLevelDesc_ruRU": self.EduLevelDesc_ruRU,
			"EduLevelName_enUS": self.EduLevelName_enUS,
			"EduLevelDesc_enUS": self.EduLevelDesc_enUS
		}
		return json_data


class Emp_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_emp_status"
	EmpStatId = db.Column("EmpStatId",db.Integer,nullable=False,primary_key=True)
	EmpStatName_tkTM = db.Column("EmpStatName_tkTM",db.String(100))#,nullable=False)
	EmpStatDesc_tkTM = db.Column("EmpStatDesc_tkTM",db.String(500))
	EmpStatName_ruRU = db.Column("EmpStatName_ruRU",db.String(100))#,nullable=False)
	EmpStatDesc_ruRU = db.Column("EmpStatDesc_ruRU",db.String(500))
	EmpStatName_enUS = db.Column("EmpStatName_enUS",db.String(100))#,nullable=False)
	EmpStatDesc_enUS = db.Column("EmpStatDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='emp_status',lazy=True)

	def to_json(self):
		json_data = {
			"EmpStatId": self.EmpStatId,
			"EmpStatName_tkTM": self.EmpStatName_tkTM,
			"EmpStatDesc_tkTM": self.EmpStatDesc_tkTM,
			"EmpStatName_ruRU": self.EmpStatName_ruRU,
			"EmpStatDesc_ruRU": self.EmpStatDesc_ruRU,
			"EmpStatName_enUS": self.EmpStatName_enUS,
			"EmpStatDesc_enUS": self.EmpStatDesc_enUS
		}
		return json_data


class Nationality(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_nationality"
	NatId = db.Column("NatId",db.Integer,nullable=False,primary_key=True)
	NatName_tkTM = db.Column("NatName_tkTM",db.String(50))#,nullable=False)
	NatDesc_tkTM = db.Column("NatDesc_tkTM",db.String(500))
	NatName_ruRU = db.Column("NatName_ruRU",db.String(50))#,nullable=False)
	NatDesc_ruRU = db.Column("NatDesc_ruRU",db.String(500))
	NatName_enUS = db.Column("NatName_enUS",db.String(50))#,nullable=False)
	NatDesc_enUS = db.Column("NatDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='nationality',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='nationality',lazy=True)

	def to_json(self):
		json_data = {
			"NatId": self.NatId,
			"NatName_tkTM": self.NatName_tkTM,
			"NatDesc_tkTM": self.NatDesc_tkTM,
			"NatName_ruRU": self.NatName_ruRU,
			"NatDesc_ruRU": self.NatDesc_ruRU,
			"NatName_enUS": self.NatName_enUS,
			"NatDesc_enUS": self.NatDesc_enUS
		}
		return json_data


class Profession(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_profession"
	ProfessionId = db.Column("ProfessionId",db.Integer,nullable=False,primary_key=True)
	ProfessionName_tkTM = db.Column("ProfessionName_tkTM",db.String(50))#,nullable=False)
	ProfessionDesc_tkTM = db.Column("ProfessionDesc_tkTM",db.String(500))
	ProfessionName_ruRU = db.Column("ProfessionName_ruRU",db.String(50))#,nullable=False)
	ProfessionDesc_ruRU = db.Column("ProfessionDesc_ruRU",db.String(500))
	ProfessionName_enUS = db.Column("ProfessionName_enUS",db.String(50))#,nullable=False)
	ProfessionDesc_enUS = db.Column("ProfessionDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='profession',lazy=True)

	def to_json(self):
		json_data = {
			"ProfessionId": self.ProfessionId,
			"ProfessionName_tkTM": self.ProfessionName_tkTM,
			"ProfessionDesc_tkTM": self.ProfessionDesc_tkTM,
			"ProfessionName_ruRU": self.ProfessionName_ruRU,
			"ProfessionDesc_ruRU": self.ProfessionDesc_ruRU,
			"ProfessionName_enUS": self.ProfessionName_enUS,
			"ProfessionDesc_enUS": self.ProfessionDesc_enUS
		}
		return json_data


class Rel_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rel_status"
	RelStatId = db.Column("RelStatId",db.Integer,nullable=False,primary_key=True)
	RelStatName_tkTM = db.Column("RelStatName_tkTM",db.String(50))#,nullable=False)
	RelStatDesc_tkTM = db.Column("RelStatDesc_tkTM",db.String(500))
	RelStatName_ruRU = db.Column("RelStatName_ruRU",db.String(50))#,nullable=False)
	RelStatDesc_ruRU = db.Column("RelStatDesc_ruRU",db.String(500))
	RelStatName_enUS = db.Column("RelStatName_enUS",db.String(50))#,nullable=False)
	RelStatDesc_enUS = db.Column("RelStatDesc_enUS",db.String(500))
	Relatives = db.relationship("Relatives",backref='rel_status',lazy=True)

	def to_json(self):
		json_data = {
			"RelStatId": self.RelStatId,
			"RelStatName_tkTM": self.RelStatName_tkTM,
			"RelStatDesc_tkTM": self.RelStatDesc_tkTM,
			"RelStatName_ruRU": self.RelStatName_ruRU,
			"RelStatDesc_ruRU": self.RelStatDesc_ruRU,
			"RelStatName_enUS": self.RelStatName_enUS,
			"RelStatDesc_enUS": self.RelStatDesc_enUS
		}
		return json_data


class Relatives(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_relatives"
	RelId = db.Column("RelId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RelStatId = db.Column("RelStatId",db.Integer,db.ForeignKey("tbl_dk_rel_status.RelStatId"))
	RelPersonName = db.Column("RelPersonName",db.String(100),nullable=False)
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	RelBirthDate = db.Column("RelBirthDate",db.DateTime)
	RelBirthPlace = db.Column("RelBirthPlace",db.String(255))
	RelWorkPlace = db.Column("RelWorkPlace",db.String(255))
	RelWorkPosition = db.Column("RelWorkPosition",db.String(255))
	RelResidence = db.Column("RelResidence",db.String(255))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
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
		return json_data


class School(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_school"
	SchoolId = db.Column("SchoolId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	SchoolTypeId = db.Column("SchoolTypeId",db.Integer,db.ForeignKey("tbl_dk_school_type.SchoolTypeId"))
	SchoolName = db.Column("SchoolName",db.String(255),nullable=False)
	SchoolDesc = db.Column("SchoolDesc",db.String(500))
	SchoolPlace = db.Column("SchoolPlace",db.String(255))
	SchoolEduStartDate = db.Column("SchoolEduStartDate",db.DateTime)
	SchoolEduEndDate = db.Column("SchoolEduEndDate",db.DateTime)
	SchoolProfession = db.Column("SchoolProfession",db.String(255))
	SchoolIsGraduated = db.Column("SchoolIsGraduated",db.Boolean,default=False)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
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
		return json_data


class School_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_school_type"
	SchoolTypeId = db.Column("SchoolTypeId",db.Integer,nullable=False,primary_key=True)
	SchoolTypeName_tkTM = db.Column("SchoolTypeName_tkTM",db.String(50))#,nullable=False)
	SchoolTypeDesc_tkTM = db.Column("SchoolTypeDesc_tkTM",db.String(500))
	SchoolTypeName_ruRU = db.Column("SchoolTypeName_ruRU",db.String(50))#,nullable=False)
	SchoolTypeDesc_ruRU = db.Column("SchoolTypeDesc_ruRU",db.String(500))
	SchoolTypeName_enUS = db.Column("SchoolTypeName_enUS",db.String(50))#,nullable=False)
	SchoolTypeDesc_enUS = db.Column("SchoolTypeDesc_enUS",db.String(500))	


# !!! changed
class Visited_countries(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_visited_countries"
	VCId = db.Column("VCId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	VCCountryName = db.Column("VCCountryName",db.String(50),nullable=False)
	VCCountryDesc = db.Column("VCCountryDesc",db.String(500))
	VCPurpose = db.Column("VCPurpose",db.String(500))
	VCStartDate = db.Column("VCStartDate",db.DateTime)
	VCEndDate = db.Column("VCEndDate",db.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
			"vcId": self.VCId,
			"empId": self.EmpId,
			"vcCountryName": self.VCCountryName,
			"vcCountryDesc": self.VCCountryDesc,
			"vcPurpose": self.VCPurpose,
			"vcStartDate": self.VCStartDate,
			"vcEndDate": self.VCEndDate
		}
		return json_data


class Work_history(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_work_history"
	WorkHistId = db.Column("WorkHistId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	WorkHistoryWorkPlace = db.Column("WorkHistoryWorkPlace",db.String(100),nullable=False)
	WorkHistoryWorkDesc = db.Column("WorkHistoryWorkDesc",db.String(500))
	WorkHistoryWorkDept = db.Column("WorkHistoryWorkDept",db.String(255))
	WorkHistoryWorkPos = db.Column("WorkHistoryWorkPos",db.String(255))
	WorkHistoryWorkStartDate = db.Column("WorkHistoryWorkStartDate",db.DateTime)
	WorkHistoryWorkEndDate = db.Column("WorkHistoryWorkEndDate",db.DateTime)
	WorkHistoryWorkEndReason = db.Column("WorkHistoryWorkEndReason",db.String(500))
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
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
		return json_data