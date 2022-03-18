from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import AddInf, BaseModel


class Res_collection_line(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_res_collection_line"
	ResCollectionLineId = db.Column("ResCollectionLineId",db.Integer,nullable=False,primary_key=True)
	ResCollectionLineGuid = db.Column("ResCollectionLineGuid",UUID(as_uuid=True),unique=True)
	ResCollectionId = db.Column("ResCollectionId",db.Integer,db.ForeignKey("tbl_dk_res_collection.ResCollectionId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResCollectionLineAmount = db.Column("ResCollectionLineAmount",db.Float,nullable=False,default=0)
	ResCollectionLinePrice = db.Column("ResCollectionLinePrice",db.Float)
	ResCollectionLineDesc = db.Column("ResCollectionLineDesc",db.String(500),default='')

	def to_json_api(self):
		data = {
			"ResCollectionLineId": self. ResCollectionLineId,
			"ResCollectionLineGuid": self. ResCollectionLineGuid,
			"ResCollectionId": self.ResCollectionId,
			"UnitId": self.UnitId,
			"ResId": self.ResId,
			"ResCollectionLineAmount": self. ResCollectionLineAmount,
			"ResCollectionLinePrice": self. ResCollectionLinePrice,
			"ResCollectionLineDesc": self. ResCollectionLineDesc
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data