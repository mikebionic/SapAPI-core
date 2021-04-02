from main_pack import db
from main_pack.models import BaseModel


class Language(BaseModel, db.Model):
	__tablename__ = "tbl_dk_language"
	LangId = db.Column("LangId",db.Integer,nullable=False,primary_key=True)
	LangName = db.Column("LangName",db.String(100),nullable=False)
	LangDesc = db.Column("LangDesc",db.String(500))
	Res_translations = db.relationship("Res_translations",backref='language',lazy=True)

	def to_json_api(self):
		data = {
			"LangId": self.LangId,
			"LangName": self.LangName,
			"LangDesc": self.LangDesc
		}
		return data