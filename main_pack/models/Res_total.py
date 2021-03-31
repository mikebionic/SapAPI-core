
class Res_total(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_total"
	ResTotId = db.Column("ResTotId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	ResTotBalance = db.Column("ResTotBalance",db.Float,default=0.0)
	ResTotInAmount = db.Column("ResTotInAmount",db.Float,default=0.0)
	ResPendingTotalAmount = db.Column("ResPendingTotalAmount",db.Float,default=0.0)
	ResTotOutAmount = db.Column("ResTotOutAmount",db.Float,default=0.0)
	ResTotLastTrDate = db.Column("ResTotLastTrDate",db.DateTime,default=datetime.now)
	ResTotPurchAvgPrice = db.Column("ResTotPurchAvgPrice",db.Float,default=0.0)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResTotId": self.ResTotId,
			"ResId": self.ResId,
			"CurrencyId": self.CurrencyId,
			"WhId": self.WhId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WpId": self.WpId,
			"ResTotBalance": self.ResTotBalance,
			"ResTotInAmount": self.ResTotInAmount,
			"ResPendingTotalAmount": self.ResPendingTotalAmount,
			"ResTotOutAmount": self.ResTotOutAmount,
			"ResTotLastTrDate": apiDataFormat(self.ResTotLastTrDate),
			"ResTotPurchAvgPrice": self.ResTotPurchAvgPrice,
		}
		return json_data