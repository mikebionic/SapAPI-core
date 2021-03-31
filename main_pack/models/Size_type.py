
class Size_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_size_type"
	SizeTypeId = db.Column("SizeTypeId",db.Integer,nullable=False,primary_key=True)
	SizeTypeName = db.Column("SizeTypeName",db.String(100),nullable=False)
	SizeTypeDesc = db.Column("SizeTypeDesc",db.String(500))
	Size = db.relationship("Size",backref='size_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"SizeTypeName": self.SizeTypeName,
			"SizeTypeDesc": self.SizeTypeDesc,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data