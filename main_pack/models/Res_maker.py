

class Res_maker(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_maker"
	ResMakerId = db.Column("ResMakerId",db.Integer,nullable=False,primary_key=True)
	ResMakerName = db.Column("ResMakerName",db.String(100),nullable=False)
	ResMakerDesc = db.Column("ResMakerDesc",db.String(500))
	ResMakerSite = db.Column("ResMakerSite",db.String(150))
	ResMakerMail = db.Column("ResMakerMail",db.String(100))
	ResMakerPhone1 = db.Column("ResMakerPhone1",db.String(100))
	ResMakerPhone2 = db.Column("ResMakerPhone2",db.String(100))
	Resource = db.relationship("Resource",backref='res_maker',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResMakerId": self.ResMakerId,
			"ResMakerName": self.ResMakerName,
			"ResMakerDesc": self.ResMakerDesc,
			"ResMakerSite": self.ResMakerSite,
			"ResMakerMail": self.ResMakerMail,
			"ResMakerPhone1": self.ResMakerPhone1,
			"ResMakerPhone2": self.ResMakerPhone2,
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

