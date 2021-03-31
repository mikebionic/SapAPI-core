
class Work_period(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_work_period"
	WpId = db.Column("WpId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	WpStartDate = db.Column("WpStartDate",db.DateTime)
	WpEndDate = db.Column("WpEndDate",db.DateTime)
	WpIsDefault = db.Column("WpIsDefault",db.Boolean,default=False)
	Rp_acc = db.relationship("Rp_acc",backref='work_period',lazy=True)
	Invoice = db.relationship("Invoice",backref='work_period',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='work_period',lazy=True)
	Res_total = db.relationship("Res_total",backref='work_period',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='work_period',lazy=True)
	Sale_card = db.relationship("Sale_card",backref='work_period',lazy=True)

	def to_json_api(self):
		json_data = {
			"WpId": self.WpId,
			"CId": self.CId,
			"DivId": self.DivId,
			"CurrencyId": self.CurrencyId,
			"WpStartDate": self.WpStartDate,
			"WpEndDate": self.WpEndDate,
			"WpIsDefault": self.WpIsDefault
		}
		return json_data