

class Language(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_language"
	LangId = db.Column("LangId",db.Integer,nullable=False,primary_key=True)
	LangName = db.Column("LangName",db.String(100),nullable=False)
	LangDesc = db.Column("LangDesc",db.String(500))
	Res_translations = db.relationship("Res_translations",backref='language',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_data = {
			"langId": self.LangId,
			"langName": self.LangName,
			"langDesc": self.LangDesc
		}
		return json_data