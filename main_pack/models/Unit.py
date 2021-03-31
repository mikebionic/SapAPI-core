

class Unit(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_unit"
	UnitId = db.Column("UnitId",db.Integer,nullable=False,primary_key=True)
	UnitName_tkTM = db.Column("UnitName_tkTM",db.String(100))
	UnitDesc_tkTM = db.Column("UnitDesc_tkTM",db.String(100))
	UnitName_ruRU = db.Column("UnitName_ruRU",db.String(100))
	UnitDesc_ruRU = db.Column("UnitDesc_ruRU",db.String(100))
	UnitName_enUS = db.Column("UnitName_enUS",db.String(100))
	UnitDesc_enUS = db.Column("UnitDesc_enUS",db.String(100))
	Res_unit = db.relationship("Res_unit",backref='unit',lazy=True)
	Barcode = db.relationship("Barcode",backref='unit',lazy=True)
	Resource = db.relationship("Resource",backref='unit',lazy=True)
	Inv_line = db.relationship("Inv_line",backref='unit',lazy=True)
	Order_inv_line = db.relationship("Order_inv_line",backref='unit',lazy=True)
	Res_price = db.relationship("Res_price",backref='unit',lazy=True)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='unit',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='unit',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='unit',lazy=True)
	Production_line = db.relationship("Production_line",backref='unit',lazy=True)

	def to_json_api(self):
		json_data = {
			"UnitName_tkTM": self.UnitName_tkTM,
			"UnitDesc_tkTM": self.UnitDesc_tkTM,
			"UnitName_ruRU": self.UnitName_ruRU,
			"UnitDesc_ruRU": self.UnitDesc_ruRU,
			"UnitName_enUS": self.UnitName_enUS,
			"UnitDesc_enUS": self.UnitDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data