from main_pack import db
from main_pack.models import BaseModel


class Password_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_password_type"
	PsswTypeId = db.Column("PsswTypeId",db.Integer,nullable=False,primary_key=True)
	PsswTypeName = db.Column("PsswTypeName",db.String(100),nullable=False)
	PsswTypeDesc = db.Column("PsswTypeDesc",db.String(500))
	Password = db.relationship("Password",backref='password_type',lazy=True)

	def to_json_api(self):
		data = {
			"PsswTypeId": self.PsswTypeId,
			"PsswTypeName": self.PsswTypeName,
			"PsswTypeDesc": self.PsswTypeDesc
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data