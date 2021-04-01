
class Barcode(BaseModel, db.Model):
	__tablename__ = "tbl_dk_barcode"
	BarcodeId = db.Column("BarcodeId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BarcodeVal = db.Column("BarcodeVal",db.String(100),nullable=False)

	def to_json_api(self):
		json_data = {
			"BarcodeId": self.BarcodeId,
			"CId": self.CId,
			"DivId": self.DivId,
			"ResId": self.ResId,
			"UnitId": self.UnitId,
			"BarcodeVal": self.BarcodeVal,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data
