
class Color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_color"
	ColorId = db.Column("ColorId",db.Integer,nullable=False,primary_key=True)
	ColorName = db.Column("ColorName",db.String(100),nullable=False)
	ColorDesc = db.Column("ColorDesc",db.String(500))
	ColorCode = db.Column("ColorCode",db.String(100))
	Res_color = db.relationship("Res_color",backref='color',lazy=True)
	Translations = db.relationship("Translations",backref='color',lazy=True)


	def to_json_api(self):
		json_data = {
			"ColorName": self.ColorName,
			"ColorDesc": self.ColorDesc,
			"ColorCode": self.ColorCode,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data
