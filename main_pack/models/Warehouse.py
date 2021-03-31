
class Warehouse(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_warehouse"
	WhId = db.Column("WhId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	WhName = db.Column("WhName",db.String(100),nullable=False)
	WhDesc = db.Column("WhDesc",db.String(500))
	WhGuid = db.Column("WhGuid",UUID(as_uuid=True),unique=True)
	Res_transaction = db.relationship("Res_transaction",backref='warehouse',lazy=True)
	Invoice = db.relationship("Invoice",backref='warehouse',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='warehouse',lazy=True)
	Res_total = db.relationship("Res_total",backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",foreign_keys='Res_trans_inv.WhIdIn',backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",foreign_keys='Res_trans_inv.WhIdOut',backref='warehouse',lazy=True)
	Production = db.relationship("Production",foreign_keys='Production.WhIdIn',backref='warehouse',lazy=True)
	Production = db.relationship("Production",foreign_keys='Production.WhIdOut',backref='warehouse',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"WhId": self.WhId,
			"CId": self.CId,
			"DivId": self.DivId,
			"UsageStatusId": self.UsageStatusId,
			"WhName": self.WhName,
			"WhDesc": self.WhDesc,
			"WhGuid": self.WhGuid,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data