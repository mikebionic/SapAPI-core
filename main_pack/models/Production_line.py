
class Production_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_production_line"
	ProdLineId = db.Column("ProdLineId",db.Integer,nullable=False,primary_key=True)
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ProdLineAmount = db.Column("ProdLineAmount",db.Float,nullable=False,default=0)
	ProdLinePrice = db.Column("ProdLinePrice",db.Float)
	ProdLineDesc = db.Column("ProdLineDesc",db.String(500),default='')

	def to_json_api(self):
		json_data = {
			"ProdLineId": self.ProdLineId,
			"ProdId": self.ProdId,
			"UnitId": self.UnitId,
			"ResId": self.ResId,
			"ProdLineAmount": self.ProdLineAmount,
			"ProdLinePrice": self.ProdLinePrice,
			"ProdLineDesc": self.ProdLineDesc
		}
		return json_data
