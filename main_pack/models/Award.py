from main_pack import db
from main_pack.models import AddInf, BaseModel
from main_pack.base.dataMethods import apiDataFormat


class Award(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_award"
	AwardId = db.Column("AwardId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	AwardName = db.Column("AwardName",db.String(100),nullable=False)
	AwardDesc = db.Column("AwardDesc",db.String(500))
	AwardRecievedDate = db.Column("AwardRecievedDate",db.DateTime)

	def to_json_api(self):
		data = {
			"AwardId": self.AwardId,
			"EmpId": self.EmpId,
			"AwardName": self.AwardName,
			"AwardDesc": self.AwardDesc,
			"AwardRecievedDate": apiDataFormat(self.AwardRecievedDate)
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data