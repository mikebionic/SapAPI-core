
class Production(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_production"
	ProdId = db.Column("ProdId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhIdIn = db.Column("WhIdIn",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WhIdOut = db.Column("WhIdOut",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ProdName = db.Column("ProdName",db.String(100),nullable=False)
	ProdDesc = db.Column("ProdDesc",db.String(500),default='')
	ProdTime = db.Column("ProdTime",db.Float)
	ProdCostPrice = db.Column("ProdCostPrice",db.Float)
	Production_line = db.relationship("Production_line",backref='production',lazy=True)
	Image = db.relationship("Image",backref='production',lazy=True)
	Translations = db.relationship("Translations",backref='production',lazy=True)

	def to_json_api(self):
		json_data = {
			"ProdId": self.ProdId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhIdIn": self.WhIdIn,
			"WhIdOut": self.WhIdOut,
			"ResId": self.ResId,
			"ProdName": self.ProdName,
			"ProdDesc": self.ProdDesc,
			"ProdTime": self.ProdTime,
			"ProdCostPrice": self.ProdCostPrice
		}
		return json_data
