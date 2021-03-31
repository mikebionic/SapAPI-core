
class Inv_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_line"
	InvLineId = db.Column("InvLineId",db.Integer,nullable=False,primary_key=True)
	InvLineGuid = db.Column("InvLineGuid",UUID(as_uuid=True),unique=True)
	InvId = db.Column("InvId",db.Integer,db.ForeignKey("tbl_dk_invoice.InvId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column("LastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	InvLineRegNo = db.Column("InvLineRegNo",db.String(100),nullable=False,unique=True)
	InvLineDesc = db.Column("InvLineDesc",db.String(500))
	InvLineAmount = db.Column("InvLineAmount",db.Float)
	InvLinePrice = db.Column("InvLinePrice",db.Float,default=0.0)
	InvLineTotal = db.Column("InvLineTotal",db.Float,default=0.0)
	InvLineExpenseAmount = db.Column("InvLineExpenseAmount",db.Float,default=0.0)
	InvLineTaxAmount = db.Column("InvLineTaxAmount",db.Float,default=0.0)
	InvLineDiscAmount = db.Column("InvLineDiscAmount",db.Float,default=0.0)
	InvLineFTotal = db.Column("InvLineFTotal",db.Float,default=0.0)
	InvLineDate = db.Column("InvLineDate",db.DateTime,default=datetime.now)
	ExcRateValue = db.Column("ExcRateValue",db.Float,default=0.0)
	Inv_line_det = db.relationship("Inv_line_det",backref='inv_line',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='inv_line',lazy=True)
	# Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='inv_line',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		inv_line = {
			"InvLineId": self.InvLineId,
			"InvLineGuid": self.InvLineGuid,
			"InvId": self.InvId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"LastVendorId": self.LastVendorId,
			"InvLineDesc": self.InvLineDesc,
			"InvLineAmount": self.InvLineAmount,
			"InvLinePrice": self.InvLinePrice,
			"InvLineTotal": self.InvLineTotal,
			"InvLineExpenseAmount": self.InvLineExpenseAmount,
			"InvLineTaxAmount": self.InvLineTaxAmount,
			"InvLineDiscAmount": self.InvLineDiscAmount,
			"InvLineFTotal": self.InvLineFTotal,
			"InvLineDate": self.InvLineDate,
			"ExcRateValue": self.ExcRateValue,
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
		return inv_line
