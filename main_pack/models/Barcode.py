from main_pack import db
from main_pack.models import BaseModel


class Barcode(BaseModel, db.Model):
	__tablename__ = "tbl_dk_barcode"
	BarcodeId = db.Column("BarcodeId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BarcodeVal = db.Column("BarcodeVal",db.String(100),nullable=False)

	def to_json_api(self):
		data = {
			"BarcodeId": self.BarcodeId,
			"CId": self.CId,
			"DivId": self.DivId,
			"ResId": self.ResId,
			"UnitId": self.UnitId,
			"BarcodeVal": self.BarcodeVal
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data
