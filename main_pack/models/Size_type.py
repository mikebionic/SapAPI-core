from main_pack import db
from main_pack.models import BaseModel


class Size_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_size_type"
	SizeTypeId = db.Column("SizeTypeId",db.Integer,nullable=False,primary_key=True)
	SizeTypeName = db.Column("SizeTypeName",db.String(100),nullable=False)
	SizeTypeDesc = db.Column("SizeTypeDesc",db.String(500))
	Size = db.relationship("Size",backref='size_type',lazy=True)

	def to_json_api(self):
		data = {
			"SizeTypeName": self.SizeTypeName,
			"SizeTypeDesc": self.SizeTypeDesc,
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data