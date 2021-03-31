

class Sl_image(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sl_image"
	SlImgId = db.Column("SlImgId",db.Integer,nullable=False,primary_key=True)
	SlId = db.Column("SlId",db.Integer,db.ForeignKey("tbl_dk_slider.SlId"))
	SlImgTitle = db.Column("SlImgTitle",db.String(100))
	SlImgDesc = db.Column("SlImgDesc",db.String(500),default='')
	SlImgLink = db.Column("SlImgLink",db.String(100))
	# "SlImgMainImg" bytea,
	SlImgMainImgFileName = db.Column("SlImgMainImgFileName",db.String(255),default='')
	SlImgMainImgFilePath = db.Column("SlImgMainImgFilePath",db.String(255),default='')
	SlImgSubImageFileName1 = db.Column("SlImgSubImageFileName1",db.String(255),default='')
	SlImgSubImageFilePath1 = db.Column("SlImgSubImageFilePath1",db.String(255),default='')
	SlImgSubImageFileName2 = db.Column("SlImgSubImageFileName2",db.String(255),default='')
	SlImgSubImageFilePath2 = db.Column("SlImgSubImageFilePath2",db.String(255),default='')
	SlImgSubImageFileName3 = db.Column("SlImgSubImageFileName3",db.String(255),default='')
	SlImgSubImageFilePath3 = db.Column("SlImgSubImageFilePath3",db.String(255),default='')
	SlImgSubImageFileName4 = db.Column("SlImgSubImageFileName4",db.String(255),default='')
	SlImgSubImageFilePath4 = db.Column("SlImgSubImageFilePath4",db.String(255),default='')
	SlImgSubImageFileName5 = db.Column("SlImgSubImageFileName5",db.String(255),default='')
	SlImgSubImageFilePath5 = db.Column("SlImgSubImageFilePath5",db.String(255),default='')
	SlImgStartDate = db.Column("SlImgStartDate",db.DateTime,default=datetime.now)
	SlImgEndDate = db.Column("SlImgEndDate",db.DateTime)
	Translations = db.relationship("Translations",backref='sl_image',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"SlImgId": self.SlImgId,
			"SlId": self.SlId,
			"SlImgTitle": self.SlImgTitle,
			"SlImgDesc": self.SlImgDesc,
			"SlImgLink": self.SlImgLink,
			"SlImgMainImgFileName": self.SlImgMainImgFileName,
			"SlImgMainImgFilePathS": fileToURL(file_type="slider",file_size='S',file_name=self.SlImgMainImgFileName),
			"SlImgMainImgFilePathM": fileToURL(file_type="slider",file_size='M',file_name=self.SlImgMainImgFileName),
			"SlImgMainImgFilePathR": fileToURL(file_type="slider",file_size='R',file_name=self.SlImgMainImgFileName),
			"SlImgSubImageFileName1": self.SlImgSubImageFileName1,
			"SlImgSubImageFilePath1": self.SlImgSubImageFilePath1,
			"SlImgSubImageFileName2": self.SlImgSubImageFileName2,
			"SlImgSubImageFilePath2": self.SlImgSubImageFilePath2,
			"SlImgSubImageFileName3": self.SlImgSubImageFileName3,
			"SlImgSubImageFilePath3": self.SlImgSubImageFilePath3,
			"SlImgSubImageFileName4": self.SlImgSubImageFileName4,
			"SlImgSubImageFilePath4": self.SlImgSubImageFilePath4,
			"SlImgSubImageFileName5": self.SlImgSubImageFileName5,
			"SlImgSubImageFilePath5": self.SlImgSubImageFilePath5,
			"SlImgStartDate": apiDataFormat(self.SlImgStartDate),
			"SlImgEndDate": apiDataFormat(self.SlImgEndDate),
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