
class Res_translations(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_translations"
	ResTransId = db.Column("ResTransId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LangId = db.Column("LangId",db.Integer,db.ForeignKey("tbl_dk_language.LangId"))
	ResName = db.Column("ResName",db.String(255))
	ResDesc = db.Column("ResDesc",db.String(500))
	ResFullDesc = db.Column("ResFullDesc",db.String(1500))

	def to_json_api(self):
		json_data = {
			"ResTransId": self.ResTransId,
			"ResId": self.ResId,
			"LangId": self.LangId,
			"ResName": self.ResName,
			"ResDesc": self.ResDesc,
			"ResFullDesc": self.ResFullDesc
		}
		return json_data