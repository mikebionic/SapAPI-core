
class Payment_method(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_payment_method"
	PmId = db.Column("PmId",db.Integer,nullable=False,primary_key=True)	
	PmName = db.Column("PmName",db.String(100),nullable=False)
	PmDesc = db.Column("PmDesc",db.String(500))
	PmVisibleIndex = db.Column("PmVisibleIndex",db.Integer,default=0)
	Order_inv = db.relationship("Order_inv",backref='payment_method',lazy=True)
	Invoice = db.relationship("Invoice",backref='payment_method',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		payment_method = {
			"PmId": self.PmId,			
			"PmName": self.PmName,
			"PmDesc": self.PmDesc,
			"PmVisibleIndex": self.PmVisibleIndex,
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
		return payment_method