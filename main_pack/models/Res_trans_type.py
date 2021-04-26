from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import BaseModel


class Res_trans_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_res_trans_type"
	ResTransTypeId = db.Column("ResTransTypeId",db.Integer,nullable=False,primary_key=True)
	ResTrTypeGuid = db.Column("ResTrTypeGuid",UUID(as_uuid=True),unique=True)
	ResTransTypeName_tkTM = db.Column("ResTransTypeName_tkTM",db.String(100),nullable=False)
	ResTransTypeDesc_tkTM = db.Column("ResTransTypeDesc_tkTM",db.String(500))
	ResTransTypeName_ruRU = db.Column("ResTransTypeName_ruRU",db.String(100))
	ResTransTypeDesc_ruRU = db.Column("ResTransTypeDesc_ruRU",db.String(500))
	ResTransTypeName_enUS = db.Column("ResTransTypeName_enUS",db.String(100))
	ResTransTypeDesc_enUS = db.Column("ResTransTypeDesc_enUS",db.String(500))
	Res_transaction = db.relationship("Res_transaction",backref='res_trans_type',lazy=True)

	def to_json_api(self):
		data = {
			"ResTransTypeId": self.ResTransTypeId,
			"ResTrTypeGuid": self.ResTrTypeGuid,
			"ResTransTypeName_tkTM": self.ResTransTypeName_tkTM,
			"ResTransTypeDesc_tkTM": self.ResTransTypeDesc_tkTM,
			"ResTransTypeName_ruRU": self.ResTransTypeName_ruRU,
			"ResTransTypeDesc_ruRU": self.ResTransTypeDesc_ruRU,
			"ResTransTypeName_enUS": self.ResTransTypeName_enUS,
			"ResTransTypeDesc_enUS": self.ResTransTypeDesc_enUS
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data