
class Currency(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_currency"
	CurrencyId = db.Column("CurrencyId",db.Integer,nullable=False,primary_key=True)
	CurrencyName_tkTM = db.Column("CurrencyName_tkTM",db.String(100),nullable=False)
	CurrencyDesc_tkTM = db.Column("CurrencyDesc_tkTM",db.String(500))
	CurrencyName_ruRU = db.Column("CurrencyName_ruRU",db.String(100),nullable=False)
	CurrencyDesc_ruRU = db.Column("CurrencyDesc_ruRU",db.String(500))
	CurrencyName_enUS = db.Column("CurrencyName_enUS",db.String(100),nullable=False)
	CurrencyDesc_enUS = db.Column("CurrencyDesc_enUS",db.String(500))
	CurrencyCode = db.Column("CurrencyCode",db.String(100))
	CurrencySymbol = db.Column("CurrencySymbol",db.String(100))
	Accounting_info = db.relationship("Accounting_info",backref='currency',lazy=True)
	Exc_rate = db.relationship("Exc_rate",backref='currency',lazy=True)
	Inv_line = db.relationship("Inv_line",backref='currency',lazy=True)
	Invoice = db.relationship("Invoice",backref='currency',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='currency',lazy=True)
	Order_inv_line = db.relationship("Order_inv_line",backref='currency',lazy=True)
	Res_price = db.relationship("Res_price",backref='currency',lazy=True)
	Res_total = db.relationship("Res_total",backref='currency',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",backref='currency',lazy=True)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='currency',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='currency',lazy=True)
	Rp_acc_trans_total = db.relationship("Rp_acc_trans_total",backref='currency',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='currency',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='currency',lazy=True)
	Sale_agreement = db.relationship("Sale_agreement",backref='currency',lazy=True)
	Sale_card = db.relationship("Sale_card",backref='currency',lazy=True)
	Work_period = db.relationship("Work_period",backref='currency',lazy=True)

	def to_json_api(self):
		json_data = {
			"CurrencyId": self.CurrencyId,
			"CurrencyName_tkTM": self.CurrencyName_tkTM,
			"CurrencyDesc_tkTM": self.CurrencyDesc_tkTM,
			"CurrencyName_ruRU": self.CurrencyName_ruRU,
			"CurrencyDesc_ruRU": self.CurrencyDesc_ruRU,
			"CurrencyName_enUS": self.CurrencyName_enUS,
			"CurrencyDesc_enUS": self.CurrencyDesc_enUS,
			"CurrencyCode": self.CurrencyCode,
			"CurrencySymbol": self.CurrencySymbol,
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
		return json_data