
class Order_inv_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_order_inv_type"
	OInvTypeId = db.Column("OInvTypeId",db.Integer,nullable=False,primary_key=True)
	OInvTypeName_tkTM = db.Column("OInvTypeName_tkTM",db.String(100),nullable=False)
	OInvTypeDesc_tkTM = db.Column("OInvTypeDesc_tkTM",db.String(500))
	OInvTypeName_ruRU = db.Column("OInvTypeName_ruRU",db.String(100))
	OInvTypeDesc_ruRU = db.Column("OInvTypeDesc_ruRU",db.String(500))
	OInvTypeName_enUS = db.Column("OInvTypeName_enUS",db.String(100))
	OInvTypeDesc_enUS = db.Column("OInvTypeDesc_enUS",db.String(500))
	Order_inv = db.relationship("Order_inv",backref='order_inv_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"OInvTypeId": self.OInvTypeId,
			"OInvTypeName_tkTM": self.OInvTypeName_tkTM,
			"OInvTypeDesc_tkTM": self.OInvTypeDesc_tkTM,
			"OInvTypeName_ruRU": self.OInvTypeName_ruRU,
			"OInvTypeDesc_ruRU": self.OInvTypeDesc_ruRU,
			"OInvTypeName_enUS": self.OInvTypeName_enUS,
			"OInvTypeDesc_enUS": self.OInvTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data
