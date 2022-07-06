from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import AddInf, BaseModel


class Res_collection(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_res_collection"
	ResCollectionId = db.Column("ResCollectionId",db.Integer,nullable=False,primary_key=True)
	ResCollectionGuid = db.Column("ResCollectionGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResCollectionName = db.Column("ResCollectionName",db.String(100),nullable=False)
	ResCollectionDesc = db.Column("ResCollectionDesc",db.String(500),default='')
	ResCollectionPrice = db.Column("ResCollectionPrice",db.Float)
	Res_collection_line = db.relationship("Res_collection_line",backref='res_collection',lazy=True)
	Image = db.relationship("Image",backref='res_collection',lazy=True)

	def to_json_api(self):
		data = {
			"ResCollectionId": self.ResCollectionId,
			"ResCollectionGuid": self.ResCollectionGuid,
			"CId": self.CId,
			"DivId": self.DivId,
			"ResCollectionName": self.ResCollectionName,
			"ResCollectionDesc": self.ResCollectionDesc,
			"ResCollectionPrice": self.ResCollectionPrice
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data