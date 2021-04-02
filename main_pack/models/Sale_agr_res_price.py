from main_pack import db
from main_pack.models import BaseModel


class Sale_agr_res_price(BaseModel, db.Model):
	__tablename__ = "tbl_dk_sale_agr_res_price"
	SAResPriceId = db.Column("SAResPriceId",db.Integer,nullable=False,primary_key=True)
	SaleAgrId = db.Column("SaleAgrId",db.Integer,db.ForeignKey("tbl_dk_sale_agreement.SaleAgrId"))
	ResPriceTypeId = db.Column("ResPriceTypeId",db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SAResPriceRegNo = db.Column("SAResPriceRegNo",db.String(100),nullable=False)
	SAResPriceValue = db.Column("SAResPriceValue",db.Float,default=0.0)
	SAPriceStartDate = db.Column("SAPriceStartDate",db.DateTime)
	SAPriceEndDate = db.Column("SAPriceEndDate",db.DateTime)

	def to_json_api(self):
		data = {
			"SAResPriceId": self.SAResPriceId,
			"SaleAgrId": self.SaleAgrId,
			"ResPriceTypeId": self.ResPriceTypeId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"SAResPriceRegNo": self.SAResPriceRegNo,
			"SAResPriceValue": self.SAResPriceValue,
			"SAPriceStartDate": self.SAPriceStartDate,
			"SAPriceEndDate": self.SAPriceEndDate
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data