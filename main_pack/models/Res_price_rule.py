from main_pack import db
from main_pack.models import AddInf, BaseModel


class Res_price_rule(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_res_price_rule"
	RprId = db.Column("RprId",db.Integer,nullable=False,primary_key=True)
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	ResMinAmount = db.Column("ResMinAmount",db.Float)
	ResMaxAmount = db.Column("ResMaxAmount",db.Float)

	def to_json_api(self):
		data = {
			"RprId": self.RprId,
			"UsageStatusId": self.UsageStatusId,
			"ResId": self.ResId,
			"ResPriceGroupId": self.ResPriceGroupId,
			"ResMinAmount": self.ResMinAmount,
			"ResMaxAmount": self.ResMaxAmount
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data