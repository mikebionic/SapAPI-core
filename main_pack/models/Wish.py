from main_pack import db
from main_pack.models import AddInf, BaseModel


class Wish(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_wish"
	WishId = db.Column("WishId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))

	def to_json_api(self):
		data = {
			"WishId": self.WishId,
			"CId": self.CId,
			"DivId": self.DivId,
			"UId": self.UId,
			"ResId": self.ResId
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data