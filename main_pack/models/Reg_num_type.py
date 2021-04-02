from main_pack import db
from main_pack.models import BaseModel


class Reg_num_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_reg_num_type"
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeName_tkTM = db.Column("RegNumTypeName_tkTM",db.String(50),nullable=False)
	RegNumTypeDesc_tkTM = db.Column("RegNumTypeDesc_tkTM",db.String(500))
	RegNumTypeName_ruRU = db.Column("RegNumTypeName_ruRU",db.String(50),nullable=False)
	RegNumTypeDesc_ruRU = db.Column("RegNumTypeDesc_ruRU",db.String(500))
	RegNumTypeName_enUS = db.Column("RegNumTypeName_enUS",db.String(50),nullable=False)
	RegNumTypeDesc_enUS = db.Column("RegNumTypeDesc_enUS",db.String(500))
	Reg_num = db.relationship("Reg_num",backref='reg_num_type',lazy=True)
	Pred_regnum = db.relationship("Pred_regnum",backref='reg_num_type',lazy=True)

	def to_json_api(self):
		data = {
			"BankId": self.BankId,
			"MainContId": self.MainContId,
			"MainLocId": self.MainLocId,
			"BankName": self.BankName,
			"BankDesc": self.BankDesc,
			"BankCorAcc": self.BankCorAcc,
			"BankAccBik": self.BankAccBik
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data