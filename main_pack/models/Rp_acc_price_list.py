from main_pack import db
from main_pack.models import BaseModel


class Rp_acc_price_list(BaseModel, db.Model):
	__tablename__ = "tbl_dk_rp_acc_price_list"
	RpAccPId = db.Column("RpAccPId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	UnitName = db.Column("UnitName",db.String(100))
	ResBarcode = db.Column("ResBarcode",db.String(100),nullable=False)
	ResName = db.Column("ResName",db.String(100),nullable=False)
	ResDesc = db.Column("ResDesc",db.String(500))
	RpAccPValue = db.Column("RpAccPValue",db.Float,default=0)
	RpAccPDesc = db.Column("RpAccPDesc",db.String(500))
	RpAccPStartDate = db.Column("RpAccPStartDate",db.DateTime)
	RpAccPEndDate = db.Column("RpAccPEndDate",db.DateTime)

	def to_json_api(self):
		data = {
			"RpAccPId": self.RpAccPId,
			"RpAccId": self.RpAccId,
			"UnitName": self.UnitName,
			"ResBarcode": self.ResBarcode,
			"ResName": self.ResName,
			"ResDesc": self.ResDesc,
			"RpAccPValue": self.RpAccPValue,
			"RpAccPDesc": self.RpAccPDesc,
			"RpAccPStartDate": self.RpAccPStartDate,
			"RpAccPEndDate": self.RpAccPEndDate
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data