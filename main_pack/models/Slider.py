from main_pack import db
from main_pack.models import AddInf, BaseModel


class Slider(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_slider"
	SlId = db.Column("SlId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	SlName = db.Column("SlName",db.String(100),nullable=False)
	SlDesc = db.Column("SlDesc",db.String(500),default='')
	Sl_image = db.relationship("Sl_image",backref='slider',lazy=True)

	def to_json_api(self):
		data = {
			"SlId": self.SlId,
			"CId": self.CId,
			"DivId": self.DivId,
			"SlName": self.SlName,
			"SlDesc": self.SlDesc
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data