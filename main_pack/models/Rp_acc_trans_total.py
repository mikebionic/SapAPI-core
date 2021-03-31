

class Rp_acc_trans_total(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rp_acc_trans_total"
	RpAccTrTotId = db.Column("RpAccTrTotId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccTrTotBalance = db.Column("RpAccTrTotBalance",db.Float,default=0.0)
	RpAccTrTotDebit = db.Column("RpAccTrTotDebit",db.Float,default=0.0)
	RpAccTrTotCredit = db.Column("RpAccTrTotCredit",db.Float,default=0.0)
	RpAccTrTotLastTrDate = db.Column("RpAccTrTotLastTrDate",db.DateTime,default=datetime.now)

	def to_json_api(self):
		json_data = {
			"RpAccTrTotId": self.RpAccTrTotId,
			"RpAccId": self.RpAccId,
			"CurrencyId": self.CurrencyId,
			"RpAccTrTotBalance": self.RpAccTrTotBalance,
			"RpAccTrTotDebit": self.RpAccTrTotDebit,
			"RpAccTrTotCredit": self.RpAccTrTotCredit,
			"RpAccTrTotLastTrDate": apiDataFormat(self.RpAccTrTotLastTrDate)
		}
		return json_data