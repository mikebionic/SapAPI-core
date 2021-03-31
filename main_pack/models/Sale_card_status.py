
class Sale_card_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sale_card_status"
	SaleCardStatusId = db.Column("SaleCardStatusId",db.Integer,nullable=False,primary_key=True)
	SaleCardStatusName_tkTM = db.Column("SaleCardStatusName_tkTM",db.String(100))
	SaleCardStatusDesc_tkTM = db.Column("SaleCardStatusDesc_tkTM",db.String(500))
	SaleCardStatusName_ruRU = db.Column("SaleCardStatusName_ruRU",db.String(100))
	SaleCardStatusDesc_ruRU = db.Column("SaleCardStatusDesc_ruRU",db.String(500))
	SaleCardStatusName_enUS = db.Column("SaleCardStatusName_enUS",db.String(100))
	SaleCardStatusDesc_enUS = db.Column("SaleCardStatusDesc_enUS",db.String(500))
	Sale_card = db.relationship("Sale_card",backref='sale_card_status',lazy=True)

	def to_json_api(self):
		json_data = {
			"SaleCardStatusId": self.SaleCardStatusId,
			"SaleCardStatusName_tkTM": self.SaleCardStatusName_tkTM,
			"SaleCardStatusDesc_tkTM": self.SaleCardStatusDesc_tkTM,
			"SaleCardStatusName_ruRU": self.SaleCardStatusName_ruRU,
			"SaleCardStatusDesc_ruRU": self.SaleCardStatusDesc_ruRU,
			"SaleCardStatusName_enUS": self.SaleCardStatusName_enUS,
			"SaleCardStatusDesc_enUS": self.SaleCardStatusDesc_enUS
		}
		return json_data
