
class Brand(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_brand"
	BrandId = db.Column("BrandId",db.Integer,nullable=False,primary_key=True)
	BrandName = db.Column("BrandName",db.String(100),nullable=False)
	BrandDesc = db.Column("BrandDesc",db.String(100),default="")
	BrandVisibleIndex = db.Column("BrandVisibleIndex",db.Integer,default=0)
	IsMain = db.Column("IsMain",db.Boolean,default=False)
	BrandLink1 = db.Column("BrandLink1",db.String(255))
	BrandLink2 = db.Column("BrandLink2",db.String(255))
	BrandLink3 = db.Column("BrandLink3",db.String(255))
	BrandLink4 = db.Column("BrandLink4",db.String(255))
	BrandLink5 = db.Column("BrandLink5",db.String(255))
	Resource = db.relationship("Resource",backref='brand',lazy=True)
	Image = db.relationship("Image",backref='brand',lazy=True)

	def to_json_api(self):
		json_data = {
			"BrandId": self.BrandId,
			"BrandName": self.BrandName,
			"BrandDesc": self.BrandDesc,
			"BrandVisibleIndex": self.BrandVisibleIndex,
			"IsMain": self.IsMain,
			"BrandLink1": self.BrandLink1,
			"BrandLink2": self.BrandLink2,
			"BrandLink3": self.BrandLink3,
			"BrandLink4": self.BrandLink4,
			"BrandLink5": self.BrandLink5,			
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
