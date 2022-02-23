from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import AddInf, BaseModel


class Translation(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_translations"
	TranslId = db.Column("TranslId",db.Integer,nullable=False,primary_key=True)
	TranslGuid = db.Column("TranslGuid",UUID(as_uuid=True),unique=True)
	ResCatId = db.Column("ResCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ColorId = db.Column("ColorId",db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	SlImgId = db.Column("SlImgId",db.Integer,db.ForeignKey("tbl_dk_sl_image.SlImgId"))
	LangId = db.Column("LangId",db.Integer,db.ForeignKey("tbl_dk_language.LangId"))
	TranslName = db.Column("TranslName",db.String(500))
	TranslDesc = db.Column("TranslDesc",db.String(1000))

	def to_json_api(self):
		data = {
			"TranslId": self.TranslId,
			"TranslGuid": self.TranslGuid,
			"ResCatId": self.ResCatId,
			"ColorId": self.ColorId,
			"ProdId": self.ProdId,
			"SlImgId": self.SlImgId,
			"LangId": self.LangId,
			"TranslName": self.TranslName,
			"TranslDesc": self.TranslDesc
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data