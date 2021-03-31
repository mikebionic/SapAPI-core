
class Res_transaction(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_transaction"
	ResTransId = db.Column("ResTransId",db.Integer,nullable=False,primary_key=True)
	ResTransTypeId = db.Column("ResTransTypeId",db.Integer,db.ForeignKey("tbl_dk_res_trans_type.ResTransTypeId"))
	InvLineId = db.Column("InvLineId",db.Integer,db.ForeignKey("tbl_dk_inv_line.InvLineId"))
	ResTrInvLineId = db.Column("ResTrInvLineId",db.Integer,db.ForeignKey("tbl_dk_res_trans_inv_line.ResTrInvLineId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResTransName = db.Column("ResTransName",db.String(100),nullable=False)
	ResTransDesc = db.Column("ResTransDesc",db.String(500))
	ResTransAmount = db.Column("ResTransAmount",db.Float,default=0.0)
	ResTransPrice = db.Column("ResTransPrice",db.Float,default=0.0)
	ResTransFTotalPrice = db.Column("ResTransFTotalPrice",db.Float,default=0.0)
	ResTransResBalance = db.Column("ResTransResBalance",db.Float,default=0.0)
	ResTransDate = db.Column("ResTransDate",db.DateTime)
	ResTransPurchAvgPrice = db.Column("ResTransPurchAvgPrice",db.Float,default=0.0)

	def to_json_api(self):
		json_data = {
			"ResTransId": self.ResTransId,
			"ResTransTypeId": self.ResTransTypeId,
			"InvLineId": self.InvLineId,
			"ResTrInvLineId": self.ResTrInvLineId,
			"CurrencyId": self.CurrencyId,
			"UnitId": self.UnitId,
			"WhId": self.WhId,
			"ResId": self.ResId,
			"ResTransName": self.ResTransName,
			"ResTransDesc": self.ResTransDesc,
			"ResTransAmount": self.ResTransAmount,
			"ResTransPrice": self.ResTransPrice,
			"ResTransFTotalPrice": self.ResTransFTotalPrice,
			"ResTransResBalance": self.ResTransResBalance,
			"ResTransDate": self.ResTransDate,
			"ResTransPurchAvgPrice": self.ResTransPurchAvgPrice
		}
		return json_data