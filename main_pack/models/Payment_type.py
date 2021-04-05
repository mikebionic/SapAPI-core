from main_pack import db
from main_pack.models import AddInf, BaseModel


class Payment_type(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_payment_type"
	PtId = db.Column("PtId",db.Integer,nullable=False,primary_key=True)
	PtName = db.Column("PtName",db.String(100),nullable=False)
	PtDesc = db.Column("PtDesc",db.String(500))
	PtVisibleIndex = db.Column("PtVisibleIndex",db.Integer,default=0)
	Order_inv = db.relationship("Order_inv",backref='payment_type',lazy=True)
	Invoice = db.relationship("Invoice",backref='payment_type',lazy=True)

	def to_json_api(self):
		data = {
			"PtId": self.PtId,
			"PtName": self.PtName,
			"PtDesc": self.PtDesc,
			"PtVisibleIndex": self.PtVisibleIndex
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data