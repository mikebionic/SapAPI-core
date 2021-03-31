
class Accounting_info(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_accounting_info"
	AccInfId = db.Column("AccInfId",db.Integer,primary_key=True,nullable=False)
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	BankId = db.Column("BankId",db.Integer, db.ForeignKey("tbl_dk_bank.BankId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	AccTypeId = db.Column("AccTypeId",db.Integer,db.ForeignKey("tbl_dk_acc_type.AccTypeId"))
	CId = db.Column("CId",db.Integer, db.ForeignKey("tbl_dk_company.CId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	AccInfName = db.Column("AccInfName",db.String(100),nullable=False)
	AccInfDesc = db.Column("AccInfDesc",db.String(500))
	AccInfNo = db.Column("AccInfNo",db.String(50),nullable=False)
	AccInfActive = db.Column("AccInfActive",db.Boolean,default=False)
	AccInfCreatedDate = db.Column("AccInfCreatedDate",db.DateTime)
	AccInfClosedDate = db.Column("AccInfClosedDate",db.DateTime)

	def to_json_api(self):
		json_data = {
			"AccInfId": self.AccInfId,
			"DivId": self.DivId,
			"BankId": self.BankId,
			"CurrencyId": self.CurrencyId,
			"AccTypeId": self.AccTypeId,
			"CId": self.CId,
			"RpAccId": self.RpAccId,
			"AccInfName": self.AccInfName,
			"AccInfDesc": self.AccInfDesc,
			"AccInfNo": self.AccInfNo,
			"AccInfActive": self.AccInfActive,
			"AccInfCreatedDate": apiDataFormat(self.AccInfCreatedDate),
			"AccInfClosedDate": apiDataFormat(self.AccInfClosedDate)
		}
		return json_data