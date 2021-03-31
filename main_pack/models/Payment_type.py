
class Payment_type(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_payment_type"
	PtId = db.Column("PtId",db.Integer,nullable=False,primary_key=True)
	PtName = db.Column("PtName",db.String(100),nullable=False)
	PtDesc = db.Column("PtDesc",db.String(500))
	PtVisibleIndex = db.Column("PtVisibleIndex",db.Integer,default=0)
	Order_inv = db.relationship("Order_inv",backref='payment_type',lazy=True)
	Invoice = db.relationship("Invoice",backref='payment_type',lazy=True)

	def to_json_api(self):
		payment_type = {
			"PtId": self.PtId,
			"PtName": self.PtName,
			"PtDesc": self.PtDesc,
			"PtVisibleIndex": self.PtVisibleIndex,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return payment_type

