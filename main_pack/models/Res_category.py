
class Res_category(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_category"
	ResCatId = db.Column("ResCatId",db.Integer,nullable=False,primary_key=True)
	ResOwnerCatId = db.Column("ResOwnerCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ResCatVisibleIndex = db.Column("ResCatVisibleIndex",db.Integer,default=0)
	IsMain = db.Column("IsMain",db.Boolean,default=False)
	ResCatName = db.Column("ResCatName",db.String(100),nullable=False)
	ResCatDesc = db.Column("ResCatDesc",db.String(500),default='')
	ResCatIconName = db.Column("ResCatIconName",db.String(100))
	ResCatIconFilePath = db.Column("ResCatIconFilePath",db.String(255))
	ResCatIconData = db.Column("ResCatIconData",db.String(100000))
	Resource = db.relationship("Resource",backref='res_category',lazy=True)
	Image = db.relationship("Image",backref='res_category',lazy=True)
	Translations = db.relationship("Translations",backref='res_category',lazy=True)
	Res_category = db.relationship("Res_category",remote_side=ResCatId,backref='subcategory',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResCatId": self.ResCatId,
			"ResOwnerCatId": self.ResOwnerCatId or 0,
			"ResCatVisibleIndex": self.ResCatVisibleIndex or 0,
			"IsMain": self.IsMain,
			"ResCatName": self.ResCatName,
			"ResCatDesc": self.ResCatDesc,
			"ResCatIconName": self.ResCatIconName,
			"ResCatIconFilePath": self.ResCatIconFilePath,
			"ResCatIconData": self.ResCatIconData,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data
