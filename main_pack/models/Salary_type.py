# from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import AddInf, BaseModel


# !!! TODO: SalaryTypeGuid
# ??? Where's salary table?
class Salary_type(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_salary_type"
	SalaryTypeId = db.Column("SalaryTypeId",db.Integer,nullable=False,primary_key=True)
	# SalaryTypeGuid = db.Column("SalaryTypeGuid",UUID(as_uuid=True),unique=True)
	SalaryTypeName_tkTM = db.Column("SalaryTypeName_tkTM",db.String(255))
	SalaryTypeDesc_tkTM = db.Column("SalaryTypeDesc_tkTM",db.String(1000))
	SalaryTypeName_ruRU = db.Column("SalaryTypeName_ruRU",db.String(255))
	SalaryTypeDesc_ruRU = db.Column("SalaryTypeDesc_ruRU",db.String(1000))
	SalaryTypeName_enUS = db.Column("SalaryTypeName_enUS",db.String(255))
	SalaryTypeDesc_enUS = db.Column("SalaryTypeDesc_enUS",db.String(1000))
	# Salary = db.relationship("Salary",backref='salary_type',lazy=True)

	def to_json_api(self):
		data = {
			"SalaryTypeId": self.SalaryTypeId,
			# "SalaryTypeGuid": self.SalaryTypeGuid,
			"SalaryTypeName_tkTM": self.SalaryTypeName_tkTM,
			"SalaryTypeDesc_tkTM": self.SalaryTypeDesc_tkTM,
			"SalaryTypeName_ruRU": self.SalaryTypeName_ruRU,
			"SalaryTypeDesc_ruRU": self.SalaryTypeDesc_ruRU,
			"SalaryTypeName_enUS": self.SalaryTypeName_enUS,
			"SalaryTypeDesc_enUS": self.SalaryTypeDesc_enUS
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data