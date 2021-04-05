from main_pack import db
from main_pack.models import AddInf, BaseModel


class Password(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_password"
	PsswId = db.Column("PsswId",db.Integer,nullable=False,primary_key=True)
	PsswUId = db.Column("PsswUId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	PsswTypeId = db.Column("PsswTypeId",db.Integer,db.ForeignKey("tbl_dk_password_type.PsswTypeId"))
	PsswPassHash = db.Column("PsswPassHash",db.String(255))
	PsswPassword = db.Column("PsswPasswor",db.String(100),nullable=False)

	def to_json_api(self):
		data = {
			"PsswId": self.PsswId,
			"PsswUId": self.PsswUId,
			"PsswTypeId": self.PsswTypeId,
			"PsswPassHash": self.PsswPassHash,
			"PsswPassword": self.PsswPassword
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data