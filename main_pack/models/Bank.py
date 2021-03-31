
class Bank(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_bank"
	BankId = db.Column("BankId",db.Integer,nullable=False,primary_key=True)
	MainContId = db.Column("MainContId",db.Integer,default=0)
	MainLocId = db.Column("MainLocId",db.Integer,default=0)
	BankName = db.Column("BankName",db.String(200),nullable=False)
	BankDesc = db.Column("BankDesc",db.String(500))
	BankCorAcc = db.Column("BankCorAcc",db.String(50))
	BankAccBik = db.Column("BankAccBik",db.String(50))
	Accounting_info = db.relationship("Accounting_info",backref='bank',lazy=True)
	Contact = db.relationship("Contact",backref='bank',lazy=True)
	Location = db.relationship("Location",backref='bank',lazy=True)

	def to_json_api(self):
		json_data = {
			"BankId": self.BankId,
			"MainContId": self.MainContId,
			"MainLocId": self.MainLocId,
			"BankName": self.BankName,
			"BankDesc": self.BankDesc,
			"BankCorAcc": self.BankCorAcc,
			"BankAccBik": self.BankAccBik,
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
