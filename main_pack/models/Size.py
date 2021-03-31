

class Size(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_size"
	SizeId = db.Column("SizeId",db.Integer,nullable=False,primary_key=True)
	SizeName = db.Column("SizeName",db.String(100),nullable=False)
	SizeDesc = db.Column("SizeDesc",db.String(500))
	SizeTypeId = db.Column("SizeTypeId",db.Integer,db.ForeignKey("tbl_dk_size_type.SizeTypeId"))
	Res_size = db.relationship("Res_size",backref='size',lazy=True)

	def to_json_api(self):
		json_data = {
			"SizeName": self.SizeName,
			"SizeDesc": self.SizeDesc,
			"SizeTypeId": self.SizeTypeId,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data