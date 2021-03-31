
class Slider(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_slider"
	SlId = db.Column("SlId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	SlName = db.Column("SlName",db.String(100),nullable=False)
	SlDesc = db.Column("SlDesc",db.String(500),default='')
	Sl_image = db.relationship("Sl_image",backref='slider',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"SlId": self.SlId,
			"CId": self.CId,
			"DivId": self.DivId,
			"SlName": self.SlName,
			"SlDesc": self.SlDesc,
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
