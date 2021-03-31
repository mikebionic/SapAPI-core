
class Discount_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_discount_type"
	DiscTypeId = db.Column("DiscTypeId",db.Integer,nullable=False,primary_key=True)
	DiscTypeName_tkTM = db.Column("DiscTypeName_tkTM",db.String(100),nullable=False)
	DiscTypeDesc_tkTM = db.Column("DiscTypeDesc_tkTM",db.String(500))
	DiscTypeName_ruRU = db.Column("DiscTypeName_ruRU",db.String(100))
	DiscTypeDesc_ruRU = db.Column("DiscTypeDesc_ruRU",db.String(500))
	DiscTypeName_enUS = db.Column("DiscTypeName_enUS",db.String(100))
	DiscTypeDesc = db.Column("DiscTypeDesc",db.String(500))
	Res_discount = db.relationship("Res_discount",backref='discount_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"DiscTypeId": self.DiscTypeId,
			"DiscTypeName_tkTM": self.DiscTypeName_tkTM,
			"DiscTypeDesc_tkTM": self.DiscTypeDesc_tkTM,
			"DiscTypeName_ruRU": self.DiscTypeName_ruRU,
			"DiscTypeDesc_ruRU": self.DiscTypeDesc_ruRU,
			"DiscTypeName_enUS": self.DiscTypeName_enUS,
			"DiscTypeDesc": self.DiscTypeDesc,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data