from main_pack import db
from main_pack.models import AddInf, BaseModel


class Country(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_country"
	CountryId = db.Column("CountryId",db.Integer,nullable=False,primary_key=True)
	CountryName = db.Column("CountryName",db.String(50),nullable=False)
	CountryDesc = db.Column("CountryDesc",db.String(500))
	City = db.relationship("City",backref='country',lazy=True)
	Location = db.relationship("Location",backref='country',lazy=True)

	def to_json_api(self):
		data = {
			"CountryId": self.CountryId,
			"CountryName": self.CountryName,
			"CountryDesc": self.CountryDesc
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data