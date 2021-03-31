
class Inv_line_det_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_line_det_type"
	InvLineDetTypeId = db.Column("InvLineDetTypeId",db.Integer,nullable=False,primary_key=True)
	InvLineDetTypeName_tkTM = db.Column("InvLineDetTypeName_tkTM",db.String(100),nullable=False)
	InvLineDetTypeDesc_tkTM = db.Column("InvLineDetTypeDesc_tkTM",db.String(500))
	InvLineDetTypeName_ruRU = db.Column("InvLineDetTypeName_ruRU",db.String(100))
	InvLineDetTypeDesc_ruRU = db.Column("InvLineDetTypeDesc_ruRU",db.String(500))
	InvLineDetTypeName_enUS = db.Column("InvLineDetTypeName_enUS",db.String(100))
	InvLineDetTypeDesc_enUS = db.Column("InvLineDetTypeDesc_enUS",db.String(500))
	Inv_line_det = db.relationship("Inv_line_det",backref='inv_line_det_type',lazy=True)

	def to_json_api(self):
		inv_line_det_type = {
			"InvLineDetTypeId": self.InvLineDetTypeId,
			"InvLineDetTypeName_tkTM": self.InvLineDetTypeName_tkTM,
			"InvLineDetTypeDesc_tkTM": self.InvLineDetTypeDesc_tkTM,
			"InvLineDetTypeName_ruRU": self.InvLineDetTypeName_ruRU,
			"InvLineDetTypeDesc_ruRU": self.InvLineDetTypeDesc_ruRU,
			"InvLineDetTypeName_enUS": self.InvLineDetTypeName_enUS,
			"InvLineDetTypeDesc_enUS": self.InvLineDetTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_line_det_type
